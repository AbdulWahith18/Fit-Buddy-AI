# Project Executable Files

{{HEADER:2 Marks}}

## Local Execution

### Prerequisites
- Python 3.10+
- Internet access for live Gemini mode
- Gemini API key for live AI generation

### Installation
```bash
pip install -r requirements.txt
```

### Configuration
Copy `.env.example` to `.env` and set `GOOGLE_API_KEY`.

### Run
```bash
uvicorn app.main:app --reload
```

### Demo mode
```powershell
$env:FITBUDDY_MOCK_AI="true"; uvicorn app.main:app --reload
```

### URLs
- Application: `http://127.0.0.1:8000`
- API documentation: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`
