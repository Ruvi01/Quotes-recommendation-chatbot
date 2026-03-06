# Project Report: Quotes Recommendation Chatbot using Rasa NLU

## Epic 1: Define Problem / Problem Understanding

### Story 1: Business Problem
Users searching manually for motivational or emotional-supportive quotes face delay, low relevance, and no personalization. This project solves that gap using an AI chatbot that understands intent and returns relevant quotes in real time.

### Story 2: Business Requirements
- Accurate intent recognition for quote categories.
- Engaging conversational interaction with varied responses.
- Web accessibility through a browser interface.

### Story 3: Literature Survey (Summary)
Reviewed conversational AI approaches including:
- Rule-based chatbot architectures.
- Machine learning intent classification (Rasa DIET pipeline).
- Recommendation/chatbot limitations in personalization and scalability.

### Story 4: Social and Business Impact
- Social: improves emotional well-being through 24/7 uplifting responses.
- Business: demonstrates scalable AI-based personalized content delivery.

## Epic 2: Environment Setup

### Story 1: Install Dependencies
Commands:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Story 2: Rasa Project Setup
Equivalent of `rasa init` has been implemented with a complete project structure, including config/data/domain/tests plus web integration.

## Epic 3: Data Collection and Model Building

### Story 1: User Queries (`data/nlu.yml`)
Intents: `greet`, `motivation`, `inspiration`, `love`, `funny`, `success`, `request_another`, `affirm`, `deny`, `thanks`, `goodbye`.

### Story 2: Bot Responses (`domain.yml`)
Intent-aligned response templates with multiple quote variations for each category.

### Story 3: Dialogue Design (`data/stories.yml`, `data/rules.yml`)
Story and rule definitions enforce meaningful, consistent flow.

### Story 4: Model Training
Command:
```powershell
rasa train
```

### Story 5: Model Storage and Reuse
Models are generated in `models/` and can be reused for shell testing, API serving, and deployment.

## Epic 4: Testing and Deployment

### Story 1: Shell Testing
```powershell
rasa shell
```

### Story 2: Test Stories
```powershell
rasa test
```

### Story 3: Web Deployment
- REST enabled via `credentials.yml`.
- Start server with API and CORS:
```powershell
rasa run --enable-api --cors "*"
```
- Flask frontend (`webapp/app.py`) provides browser chat UI.

### Story 4: Validation Checklist
- Backend-frontend connectivity.
- Real-time response rendering.
- Correct intent-based quote category mapping.
- Stability across continuous interactions.

## Conclusion
This implementation provides a practical, user-facing Rasa chatbot that delivers intent-based motivational content with a web interface, structured training data, and test coverage.

## Future Enhancements
- Emotion detection via sentiment models.
- Personalized recommendations from user history.
- Multilingual support.
- Voice input/output.
- Messaging platform integration.
- Dynamic quote APIs.
- Feedback/rating loop for retraining.
- Transformer-based NLU improvements.
- Cloud deployment and scalability.
- Usage analytics dashboard.
