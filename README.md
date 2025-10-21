# AskMyDoc

AskMyDoc is a small utility that lets you upload PDF documents and ask questions about their contents. The current UI is implemented with Streamlit in `app.py`.

This README describes how to set up a local environment, install the dependencies, and run the Streamlit app.

Prerequisites

- Python 3.11 or newer recommended

Quick start (PowerShell)

1. Create and activate a virtual environment:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and update values (optional):

```powershell
copy .env.example .env
```

4. Run the Streamlit app:

```powershell
streamlit run app.py
```

What the app does

- Open the page and use the sidebar to upload one or more PDF files.
- Click "Get Started" to extract text from the PDFs and run a simple chunking step using LangChain's `CharacterTextSplitter`.
- After chunking completes, the UI indicates you can now ask questions (note: the current scaffold performs extraction and chunking only; question-answering functionality can be added by wiring a retriever/LLM).

Files of interest

- `app.py` — Streamlit UI and the PDF extraction / chunking logic.
- `.env.example` — example environment variables.
- `requirements.txt` — Python dependencies (see below).
- `scripts/setup-venv.ps1` — convenience script to create a venv and install deps on Windows PowerShell.

Running tests

- There is a minimal Flask scaffold and a pytest file that verifies an example `/health` route. To run tests:

```powershell
.\.venv\Scripts\python -m pytest -q
```

Notes and next steps

- The app currently extracts text and chunks it. If you want retrieval + LLM answers, I can add a vectorstore (Chroma, FAISS) and a small QA flow.
- Don't commit secrets to the repository. Use `.env` for local development and keep `.env` in `.gitignore`.

If you want me to add CI, Docker, or switch to FastAPI, tell me which direction you'd like to take next.
