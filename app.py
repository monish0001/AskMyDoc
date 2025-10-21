import streamlit as st
from dotenv import load_dotenv
from src.pdf_utils import extract_text_from_pdfs
from src.text_processing import get_chunks
from src.vectorstore_utils import create_vectorstore
from src.chat_chain import get_conversation_chain
from src.ui import handle_user_query

load_dotenv()

def main():
    st.set_page_config(page_title="AskMyDoc", page_icon="📚")
    st.header("📚 Welcome to AskMyDoc")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    with st.sidebar:
        st.subheader("Upload PDFs")
        documents = st.file_uploader("Upload PDF(s):", accept_multiple_files=True)
        
        if st.button("Get Started"):
            if not documents:
                st.warning("Please upload at least one PDF file.")
                return
            
            with st.spinner("Extracting text..."):
                text = extract_text_from_pdfs(documents)
            st.success("✅ Text extracted.")

            with st.spinner("Splitting into chunks..."):
                chunks = get_chunks(text)
            st.success("✅ Chunking completed.")

            with st.spinner("Creating vector store..."):
                vectorstore = create_vectorstore(chunks)
            st.success("✅ Vector store ready.")

            st.session_state.conversation = get_conversation_chain(vectorstore)
            st.info("Ready! You can now ask questions below.")

    if st.session_state.conversation:
        question = st.text_input("Ask a question about your document:")
        if question:
            handle_user_query(question, st.session_state.conversation)
    else:
        st.info("Upload PDFs and click 'Get Started' to begin.")

if __name__ == "__main__":
    main()
