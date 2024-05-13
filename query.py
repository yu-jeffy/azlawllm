from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.core.response.pprint_utils import pprint_source_node
from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings
from llama_index.core import StorageContext
from llama_index.core.llms import ChatMessage
from llama_index.llms.groq import Groq

load_dotenv()

api_key = os.environ["PINECONE_API_KEY"]
GROQ_API_KEY = os.environ["GROQ_API_KEY"]

pc = Pinecone(api_key=api_key)

pinecone_index = pc.Index("lawllm") 

vector_store = PineconeVectorStore(
    pinecone_index=pinecone_index, text_key="content"
)
retriever = VectorStoreIndex.from_vector_store(vector_store).as_retriever(
    similarity_top_k=4,
    verbose=True
)

llm = Groq(model="llama3-70b-8192", api_key=GROQ_API_KEY)

nodes = retriever.retrieve("What is az 1-112?")

# Get a list of strings using get_text() for each entry in nodes
text_list = [node.get_text() for node in nodes]

# Convert the list of strings to a single string with each item on a new line
text = "\n".join(text_list)
print(text)

USER_PROMPT="What is az 1-212?"

messages = [
    ChatMessage(
        role="system", content="You are a paralegal assistant. You can ask me questions about Arizona laws. You can have me fetch the full text of a law, or provide a summary. If you don't know something or are missing information, state that you cannot answer that question."
    ),
    ChatMessage(role="user", content=f"""
                You will be provided a prompt and content will be fetched based on the prompt to assist you in answering the user prompt.
                
                Answer this user prompt: {USER_PROMPT}
                
                Using the following context:
                {text}
                """),
]
resp = llm.chat(messages)
print(resp)