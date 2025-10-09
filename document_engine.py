import os
from llama_index.core import (VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext, load_index_from_storage)
from llama_index.llms.groq import Groq as GroqLlama
# from llama_index.embeddings.huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if groq_api_key is not None:
    os.environ["GROQ_API_KEY"] = groq_api_key
else:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

Settings.llm = GroqLlama(model="openai/gpt-oss-120b", temperature=0.5, api_key=groq_api_key)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding # the HuggingFaceEmbeddings works with langchain, but not with llama_index
Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

documents = SimpleDirectoryReader('data').load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

def query_documents(user_query:str) -> str:
    return str(query_engine.query(user_query))