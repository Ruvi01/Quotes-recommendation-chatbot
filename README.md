# Quotes Recommendation Chatbot (Rasa + Flask)

This project implements a complete **Quotes Recommendation Chatbot** using **Rasa NLU/Core** and a **Flask web interface**, based on the milestones and requirements you provided.

## 1) Prerequisites

- Python 3.9 or 3.10 (recommended for Rasa 3.6.x)
- `pip`
- Virtual environment (`venv` or Conda)
- VS Code (or any IDE)

Optional:
- Anaconda Navigator

## 2) Environment Setup

### Create and activate venv (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

### Initialize and train

```powershell
rasa train
```

A trained model will be saved in `models/`.

## 3) Project Structure

- `data/nlu.yml`: intent examples (greet, motivation, inspiration, love, funny, success, etc.)
- `data/stories.yml`: conversational flows
- `data/rules.yml`: rule-based behavior and fallback
- `domain.yml`: intents, responses, session settings
- `config.yml`: NLU pipeline + policies
- `tests/test_stories.yml`: automated conversation tests
- `credentials.yml`: REST channel configuration
- `endpoints.yml`: action server endpoint
- `webapp/`: Flask UI (`app.py`, templates, static files)

## 4) Run the Chatbot

Use 2 terminals (with the virtual env active):

### Terminal 1: Start Rasa API server

```powershell
rasa run --enable-api --cors "*"
```

### Terminal 2: Start Flask web app

```powershell
python .\webapp\app.py
```

Open: `http://127.0.0.1:8000`

## 5) Testing

### Manual test in shell

```powershell
rasa shell
```

### Automated story test

```powershell
rasa test
```

## 6) Milestone Mapping

- Milestone 1 (Problem Understanding): documented in `docs/project_report.md`
- Milestone 2 (Setup): dependency and setup commands in this README
- Milestone 3 (Data + Model): `nlu.yml`, `domain.yml`, `stories.yml`, `rasa train`
- Milestone 4 (Testing + Deployment): `rasa shell`, `rasa test`, Flask web deployment

## 7) Notes

- The current chatbot is retrieval-like with predefined quote responses.
- You can extend with custom actions and external quote APIs.
- Future enhancements are documented in `docs/project_report.md`.


