from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings  # Corrected import
from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
import os

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
            strip_whitespace=True  # Corrected spelling
        )
        self.chunks = self.text.split_documents(self.documents)
        print(f"from {len(self.documents)} to {len(self.chunks)}") #corrected chunk.

    def get_embeddings(self):
        # embedder = HuggingFaceBgeEmbeddings(model_name="sentence-transformers/all-mini-L6-v2")
        embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.text_chunk = [chunk.page_content for chunk in self.chunks]
        self.chunk_embeddings = embedder.encode(self.text_chunk) #embed the chunks.
        print("convert to embeddings successfully!")
        return embedder
    
    
    def embedding_to_DB(self):
        embedder=self.get_embeddings()
        if not os.path.exists(self.persistent_directory):
            os.mkdir(self.persistent_directory)
            
        self.db= FAISS.from_documents(self.chunks   ,embedder)
        self.db.save_local(self.persistent_directory)
        print("db saved sucesfully!")
        
        
    def load_db(self):
        self.db =FAISS.load_local(self.persistent_directory,HuggingFaceBgeEmbeddings(model_name="sentence-transformers/all-mini-L6-v2"),allow_dangerous_deserialization=True)
        print("vector_db_loaded_sucessfully")
    
        
path_data = "D:/KMCT/miniproject/fakdec/Datasets"
path_db = "DB"
query = "what is that?"

obj = AI(path_data, path_db, query)
obj.load_documents()
obj.Text_Splitter()
obj.get_embeddings()
obj.embedding_to_DB()
obj.load_db()