# AskMyDoc (minimal Python scaffold)

This repository was scaffolded with a minimal Python application structure to help get started.

Quick start

1. Create a virtual environment and activate it (PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and update values as needed:

```powershell
cp .env.example .env
```

4. Run the app:

```powershell
python -m app
```

What you'll find

- `app/` - minimal Flask app with a health endpoint
- `.env.example` - example environment variables
- `requirements.txt` - pinned deps
- `README.md` - this file

Next steps

- Replace placeholders in `.env` (especially `SECRET_KEY`).
- If you have existing source files, move them into `app/` or adjust the package layout.
- Tell me preferred test commands or CI and I can add a GitHub Actions workflow.
