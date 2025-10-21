from PyPDF2 import PdfReader

def extract_text_from_pdfs(documents):
    texts = ""
    for doc in documents:
        pdf_reader = PdfReader(doc)
        for page in pdf_reader.pages:
            texts += page.extract_text() or ""
    return texts
