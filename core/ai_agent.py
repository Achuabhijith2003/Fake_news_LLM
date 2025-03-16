from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings #import the correct model.
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from google.generativeai import generative_models
from Config.config import Gemini_key
from langchain.prompts.prompt import PromptTemplate


class AI:
    def __init__(self, path_data, path_db, query):
        self.path_data = path_data
        self.db_dir = path_db
        self.query = query

    def load_documents(self):
        loader = PyPDFDirectoryLoader(self.path_data)
        self.documents = loader.load()

    def Text_Splitter(self):
        self.text = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True,
            strip_whitespace=True
        )
        self.chunks = self.text.split_documents(self.documents)
        print(f"from {len(self.documents)} to {len(self.chunks)}")

    def get_embeddings(self):
        embedder = HuggingFaceBgeEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2") #use the correct model.
        self.text_chunk = [chunk.page_content for chunk in self.chunks]
        self.chunk_embeddings = embedder.embed_documents(self.text_chunk)
        print("convert to embeddings successfully!")
        return embedder

    def embedding_to_DB(self):
        embedder = self.get_embeddings()
        if not os.path.exists(self.db_dir):
            print("creating new database")
            texts = [chunk.page_content for chunk in self.chunks]
            metadatas = [chunk.metadata for chunk in self.chunks]
            embeddings = embedder.embed_documents(texts) #use embed_documents.
            text_embeddings = list(zip(texts, embeddings))
            self.vector_store = FAISS.from_embeddings(text_embeddings, metadatas)
            self.vector_store.save_local(self.db_dir)
        else:
            print("loading existing database")
            self.vector_store = FAISS.load_local(self.db_dir, embedder, allow_dangerous_deserialization=True)

    def load_db(self):
        self.db =FAISS.load_local(self.db_dir,HuggingFaceBgeEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"),allow_dangerous_deserialization=True)
        
        print("vector_db_loaded_successfully")
        
        
    def Search_document(self):
        retrive=self.db.as_retriever(search_type="similarity",search_kwarg={"k":6})
        retrivered_doc=retrive.invoke(self.query)
        # print(f"Result from DB{retrivered_doc[0].page_content}")
        self.retrivered_doc_content=" ".join([doc.page_content for doc in retrivered_doc ])
        
        
    # promt template
    def Promt(self):
        self.promt_template=PromptTemplate(template="Read this para carefully {retrivered_doc} and Question: {query} , responed with true or false ")
        
    # using llm
    def model(self):
        llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash",verbose=True,temperature=0.1,api_key=Gemini_key)
        promt= self.promt_template.format(
            retrivered_doc=self.retrivered_doc_content,
            query=self.query
        )
        respones=llm.invoke(input=promt)
        print (respones)
        

path_data = "D:/KMCT/miniproject/fakdec/Datasets"
path_db = "DB/faiss"
# query = "is Central Economic Problems in 5 th module "

obj = AI(path_data, path_db, query=None)
# obj.load_documents()
# obj.Text_Splitter()
# obj.get_embeddings()
# obj.embedding_to_DB()
obj.load_db()
# obj.Search_document()

while True:
    promt=input("enter the query: ")
    obj.query=promt
    obj.Search_document()
    obj.Promt()
    obj.model()
