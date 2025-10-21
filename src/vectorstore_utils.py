import os
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain.vectorstores import FAISS

def create_vectorstore(chunks):
    hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
    if not hf_token:
        raise ValueError("Missing HUGGINGFACE_API_TOKEN in .env file.")
    
    embeddings = HuggingFaceEndpointEmbeddings(
        repo_id="sentence-transformers/all-MiniLM-L6-v2",
        huggingfacehub_api_token=hf_token
    )
    return FAISS.from_texts(chunks, embedding=embeddings)
