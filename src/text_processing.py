from langchain.text_splitter import CharacterTextSplitter

def get_chunks(texts, chunk_size=500, chunk_overlap=50):
    splitter = CharacterTextSplitter(
        separator="",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    return splitter.split_text(texts)
