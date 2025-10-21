import streamlit as st
from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpointEmbeddings, HuggingFaceEndpoint
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

load_dotenv()

# ----------------------------
# PDF Text Extraction
# ----------------------------
def extract_text_from_pdfs(documents):
    texts = ""
    for doc in documents:
        pdf_reader = PdfReader(doc)
        for page in pdf_reader.pages:
            texts += page.extract_text() or ""
    return texts

# ----------------------------
# Text Chunking
# ----------------------------
def get_chunks(texts, chunk_size=500, chunk_overlap=50):
    text_splitter = CharacterTextSplitter(
        separator="",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    chunks = text_splitter.split_text(texts)
    return chunks

# ----------------------------
# Vector Store Creation
# ----------------------------
def create_vectorstore(chunks):
    hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
    if not hf_token:
        raise ValueError("HUGGINGFACE_API_TOKEN not found in .env file.")
    
    embeddings = HuggingFaceEndpointEmbeddings(
        repo_id="sentence-transformers/all-MiniLM-L6-v2",
        huggingfacehub_api_token=hf_token
    )
    vectorstore = FAISS.from_texts(chunks, embedding=embeddings)
    return vectorstore

# ----------------------------
# Conversation Chain using ChatHuggingFace
# ----------------------------
def get_conversation_chain(vectorstore):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    hf_token = os.getenv("HUGGINGFACE_API_TOKEN")

    # Correct HuggingFaceEndpoint initialization
    llm_endpoint = HuggingFaceEndpoint(
        repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
        task="text-generation",
        huggingfacehub_api_token=hf_token,
        temperature=0.5,
        max_new_tokens=300
    )

    chat_model = ChatHuggingFace(llm=llm_endpoint)

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=chat_model,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

# ----------------------------
# Handle User Query
# ----------------------------
def get_user_query(question):
    if "conversation" not in st.session_state or st.session_state.conversation is None:
        st.warning("Please upload PDFs and click 'Get Started' first.")
        return
    
    response = st.session_state.conversation({"question": question})
    answer = response.get("answer", "Sorry, I couldn’t find an answer.")
    
    st.write("Answer:")
    st.write(answer)

    # Display chat history
    st.write("---")
    st.write("**Chat History:**")
    for msg in response.get("chat_history", []):
        st.write(f"**{msg.type.capitalize()}:** {msg.content}")

# ----------------------------
# Streamlit App
# ----------------------------
def main():
    st.set_page_config(page_title="AskMyDoc", page_icon="📚")
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    st.header("Welcome to AskMyDoc App 📚")
    
    # Sidebar: Upload PDFs & initialize conversation
    with st.sidebar:
        st.header("Upload PDFs")
        st.write("Upload single or multiple PDF documents to ask questions about them.")
        documents = st.file_uploader("Upload PDFs here:", accept_multiple_files=True)
        
        if st.button("Get Started"):
            if not documents:
                st.warning("Please upload at least one PDF file.")
                return
            
            with st.spinner("Extracting text from PDFs..."):
                data = extract_text_from_pdfs(documents)
                st.success("Text extraction completed.")
            
            with st.spinner("Chunking text..."):
                chunks = get_chunks(data)
                st.success("Chunking completed.")
            
            with st.spinner("Creating vector store..."):
                vectorstore = create_vectorstore(chunks)
                st.success("Vector store created successfully.")
            
            st.session_state.conversation = get_conversation_chain(vectorstore)
            st.info("You can now ask questions about your documents!")

    # Main input box
    if st.session_state.conversation:
        question = st.text_input("Enter your query here:")
        if question:
            get_user_query(question)
    else:
        st.info("Upload PDFs and click 'Get Started' to initialize the AI.")

if __name__ == "__main__":
    main()
