from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

QUOTES = {
    "motivation": [
        "It always seems impossible until it is done. - Nelson Mandela",
        "Small steps every day still move you forward.",
        "Your future is created by what you do today, not tomorrow.",
    ],
    "inspiration": [
        "Believe you can and you are halfway there. - Theodore Roosevelt",
        "Start where you are. Use what you have. Do what you can. - Arthur Ashe",
        "Turn your wounds into wisdom. - Oprah Winfrey",
    ],
    "success": [
        "Success is the sum of small efforts repeated day in and day out. - Robert Collier",
        "Do not watch the clock; do what it does. Keep going. - Sam Levenson",
        "Success usually comes to those who are too busy to be looking for it. - Henry David Thoreau",
    ],
    "money": [
        "Do not save what is left after spending, but spend what is left after saving. - Warren Buffett",
        "A budget is telling your money where to go instead of wondering where it went. - Dave Ramsey",
        "Never depend on a single income. Make investment to create a second source. - Warren Buffett",
    ],
    "love": [
        "Love recognizes no barriers. - Maya Angelou",
        "Where there is love there is life. - Mahatma Gandhi",
        "The best thing to hold onto in life is each other. - Audrey Hepburn",
    ],
    "funny": [
        "I am on a seafood diet. I see food and I eat it.",
        "Why do not scientists trust atoms? Because they make up everything.",
        "My wallet is like an onion, opening it makes me cry.",
    ],
    "life": [
        "Life is what happens when you are busy making other plans. - John Lennon",
        "In the middle of difficulty lies opportunity. - Albert Einstein",
        "The purpose of our lives is to be happy. - Dalai Lama",
    ],
    "confidence": [
        "With confidence, you have won before you have started. - Marcus Garvey",
        "Believe in yourself and you will be unstoppable.",
        "Confidence comes not from always being right but from not fearing to be wrong. - Peter T. Mcintyre",
    ],
    "hard_work": [
        "There are no secrets to success. It is the result of preparation, hard work, and learning from failure. - Colin Powell",
        "Dreams do not work unless you do. - John C. Maxwell",
        "The only place where success comes before work is in the dictionary. - Vidal Sassoon",
    ],
    "happiness": [
        "Happiness depends upon ourselves. - Aristotle",
        "Happiness is not by chance, but by choice. - Jim Rohn",
        "For every minute you are angry you lose sixty seconds of happiness. - Ralph Waldo Emerson",
    ],
}

CATEGORY_KEYWORDS = {
    "motivation": ["motivation", "motivational", "motivate"],
    "inspiration": ["inspiration", "inspire", "inspirational"],
    "success": ["success", "achievement", "goal"],
    "money": ["money", "finance", "wealth", "budget", "investment"],
    "love": ["love", "romantic", "relationship"],
    "funny": ["funny", "joke", "laugh", "humor"],
    "life": ["life", "living", "journey"],
    "confidence": ["confidence", "confident", "self belief"],
    "hard_work": ["hard work", "effort", "dedication", "hustle", "grind"],
    "happiness": ["happiness", "happy", "joy"],
}

STATE = {}


def detect_category(message: str):
    text = message.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return category
    return None


def next_quote(sender: str, category: str):
    session = STATE.setdefault(sender, {"indexes": {}, "last_category": None, "awaiting": None})
    quotes = QUOTES[category]
    index = session["indexes"].get(category, 0)
    quote = quotes[index % len(quotes)]
    session["indexes"][category] = (index + 1) % len(quotes)
    session["last_category"] = category
    session["awaiting"] = "helpful"
    return quote


def build_quote_reply(sender: str, category: str, prefix: str | None = None):
    quote = next_quote(sender, category)
    parts = [part for part in [prefix, quote, "Was this helpful?"] if part]
    return "\n\n".join(parts)


def response(reply: str, *, show_feedback: bool = False, category: str | None = None, quick_replies: list[dict] | None = None):
    payload = {"reply": reply, "show_feedback": show_feedback}
    if category:
        payload["category"] = category
    if quick_replies:
        payload["quick_replies"] = quick_replies
    return jsonify(payload)


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    message = (payload.get("message") or "").strip()
    sender = (payload.get("sender") or "web_user").strip()

    if not message:
        return response("Please type a message."), 400

    text = message.lower().strip()
    session = STATE.setdefault(sender, {"indexes": {}, "last_category": None, "awaiting": None})

    if any(phrase in text for phrase in ["bye", "goodbye", "see you", "take care"]):
        session["awaiting"] = None
        return response("Goodbye. Keep your face always toward the sunshine, and shadows will fall behind you. - Walt Whitman")

    if any(phrase in text for phrase in ["thank you", "thanks", "thanku", "thx", "thank u"]):
        session["awaiting"] = None
        return response("That is so sweet. You are very welcome. Happiness is not by chance, but by choice. - Jim Rohn")

    if any(phrase in text for phrase in ["hi", "hello", "hey", "good morning", "good evening"]):
        session["awaiting"] = None
        return response("Hey there. I hope your day is going gently so far. What kind of quote would you like today?")

    if session["awaiting"] == "helpful":
        if any(phrase in text for phrase in ["yes", "yeah", "helpful", "good"]):
            session["awaiting"] = "another"
            return response(
                "That makes me really happy. Would you like another quote from the same category?",
                quick_replies=[
                    {"label": "Yes", "message": "yes"},
                    {"label": "No", "message": "no"},
                ],
            )
        if any(phrase in text for phrase in ["no", "not helpful", "not really"]):
            session["awaiting"] = "another"
            return response(
                "No worries at all. Do you want another quote from the same category?",
                quick_replies=[
                    {"label": "Yes", "message": "yes"},
                    {"label": "No", "message": "no"},
                ],
            )
        if any(phrase in text for phrase in ["another", "one more", "next"]):
            category = session.get("last_category") or "motivation"
            return response(build_quote_reply(sender, category), show_feedback=True, category=category)

    if session["awaiting"] == "another":
        if any(phrase in text for phrase in ["yes", "yeah", "sure", "okay"]):
            category = session.get("last_category") or "motivation"
            return response(build_quote_reply(sender, category), show_feedback=True, category=category)
        if any(phrase in text for phrase in ["no", "nope"]):
            session["awaiting"] = None
            return response("Okay. I am here whenever you want a little boost later.")

    category = detect_category(text)
    if category:
        return response(build_quote_reply(sender, category), show_feedback=True, category=category)

    if "quote" in text:
        return response(build_quote_reply(sender, "motivation", "Here is a quote for you."), show_feedback=True, category="motivation")

    return response("I did not quite catch that. Try motivation, inspiration, success, money, love, funny, life, confidence, hard work, or happiness.")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
