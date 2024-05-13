from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings
from llama_index.core import StorageContext

load_dotenv()

api_key = os.environ["PINECONE_API_KEY"]

pc = Pinecone(api_key=api_key)

pinecone_index = pc.Index("lawllm") 



# global
Settings.embed_model = OpenAIEmbedding()

documents = SimpleDirectoryReader("files/Title_1/").load_data()

vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)

query_engine = index.as_query_engine()

response = query_engine.query("what is arizona 1-211 law? produce it verbatim, and then provide an easily understood summary after.")

print(response)