import chromadb
import uuid 

chroma_client = chromadb.Client()

client = chromadb.PersistentClient(path=".\DB") 

# Check if the collection exists, if not, create it
try:
    collection = client.get_collection(name="News")
except chromadb.db.base.UniqueConstraintError:
    collection = client.create_collection(name="News")

def add_data(data, url):
    try:
        collection.add(
            documents=[data],  # Ensure documents is a list
            ids=[str(uuid.uuid4())],  # Ensure ids is a list
            metadatas=[{"url": url}] ,
            # Ensure metadatas is a list
        )
    except Exception as e:
        print("Error: ", e)
        
def get_data(query):
    results = collection.query(
        query_texts=["Senior citizens in Mandaveli are finding companionship and community through weekly meetups organized by the RK Nagar Residents’ Welfare Association"],  # Chroma will embed this for you
        n_results=1  # how many results to return
    )
    print("Results: ", results)
