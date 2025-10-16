import streamlit as st
from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
load_dotenv()

def extract_text_from_pdfs(documents):
    texts = []
    for doc in documents:
        pdf_Reader=PdfReader(doc)
        for page in pdf_Reader.pages:
            texts.append(page.extract_text())
    return texts

def get_chunks(texts,chunk_size=500,chunk_overlap=50):
    text_splitter=CharacterTextSplitter(
        separator="",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    chunks=[]
    for text in texts:
        chunks.extend(text_splitter.split_text(text))
    return chunks


def main():
    st.set_page_config(page_title="Home | AskMyDoc",page_icon=":books:")
    st.header("Welcome to AskMyDoc App :books:")
    st.text_input("Enter your your query here:")
    
    
    
    with st.sidebar:
        st.header("AskMyDoc")
        st.write("Upload single or multiple documents and ask questions about them.")
        documents=st.file_uploader("Upload your PDF files here:",accept_multiple_files=True)
        if st.button("Get Started"):
            with st.spinner("Retrieving textual data from your files ...."):
                data=extract_text_from_pdfs(documents)
                # st.write(data[0])
                # st.write(data[1])
                st.success("Text retrieval completed successfully.")
            with st.spinner("Chunking process has been initiated...."):
                chunks=get_chunks(data)
                # st.write(chunks[0])
                # st.write(chunks[1])
                # st.write(chunks[2])
                st.success("Chunking process completed successfully.")
                st.info("You can now ask questions about your documents.")





if __name__ == "__main__":
    main()
