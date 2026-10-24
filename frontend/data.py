"""
QuizSphere data (OFFLINE DEMO MODE)

This file does the same job as js/data.js on the website.
The website saved everything in the browser (localStorage).
This app saves everything in one file instead: quizsphere_data.json,
which sits next to this file. Delete that file to start fresh.

Nothing is sent to a server. Real API calls can be added later,
once the backend teammate shares the endpoints.
"""

import json
import math
import time
from datetime import datetime
from pathlib import Path

SAVE_FILE = Path(__file__).parent / "quizsphere_data.json"

PASS_MARK = 50  # percent needed to pass a quiz

DEMO_USERS = [
    {"email": "student@college.edu", "password": "student123", "role": "student", "name": "Demo Student"},
    {"email": "instructor@college.edu", "password": "instructor123", "role": "instructor", "name": "Demo Instructor"},
]

DEMO_QUIZZES = [
    {
        "id": "gk-101",
        "theme": "gk",
        "title": "General Knowledge",
        "description": "Warm up with questions about the world around you.",
        "minutes": 15,
        "questions": [
            {"text": "What is the capital city of Japan?", "options": ["Seoul", "Tokyo", "Beijing", "Bangkok"], "answer": 1},
            {"text": "Which planet is known as the Red Planet?", "options": ["Venus", "Jupiter", "Mars", "Saturn"], "answer": 2},
            {"text": "How many continents are there on Earth?", "options": ["5", "6", "7", "8"], "answer": 2},
            {"text": "Which is the largest ocean?", "options": ["Atlantic", "Indian", "Arctic", "Pacific"], "answer": 3},
            {"text": "Who painted the Mona Lisa?", "options": ["Leonardo da Vinci", "Pablo Picasso", "Vincent van Gogh", "Claude Monet"], "answer": 0},
            {"text": "Which is the longest river in the world?", "options": ["Amazon", "Nile", "Yangtze", "Ganga"], "answer": 1},
            {"text": "What is the national animal of India?", "options": ["Lion", "Elephant", "Bengal Tiger", "Peacock"], "answer": 2},
            {"text": "Which gas do plants absorb from the air?", "options": ["Oxygen", "Nitrogen", "Carbon dioxide", "Hydrogen"], "answer": 2},
            {"text": "How many days are there in a leap year?", "options": ["365", "366", "364", "360"], "answer": 1},
            {"text": "Which is the smallest planet in our solar system?", "options": ["Mercury", "Mars", "Venus", "Pluto"], "answer": 0},
            {"text": "Who wrote 'Romeo and Juliet'?", "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"], "answer": 1},
            {"text": "What is the hardest natural substance?", "options": ["Gold", "Iron", "Diamond", "Quartz"], "answer": 2},
            {"text": "Which country is home to the kangaroo?", "options": ["New Zealand", "South Africa", "Australia", "Brazil"], "answer": 2},
            {"text": "What is the boiling point of water at sea level?", "options": ["90 °C", "100 °C", "110 °C", "120 °C"], "answer": 1},
            {"text": "Which is the tallest mountain in the world?", "options": ["K2", "Kangchenjunga", "Mount Everest", "Lhotse"], "answer": 2},
        ],
    },
    {
        "id": "math-101",
        "theme": "math",
        "title": "Basic Maths",
        "description": "Quick arithmetic and number sense questions.",
        "minutes": 15,
        "questions": [
            {"text": "What is 12 × 8?", "options": ["86", "96", "108", "92"], "answer": 1},
            {"text": "What is 15% of 200?", "options": ["15", "20", "30", "35"], "answer": 2},
            {"text": "What is the square root of 144?", "options": ["12", "14", "11", "16"], "answer": 0},
            {"text": "Which number is a prime number?", "options": ["21", "27", "29", "33"], "answer": 2},
            {"text": "What is 3/4 written as a decimal?", "options": ["0.34", "0.75", "0.43", "0.70"], "answer": 1},
            {"text": "What is 7 × 9?", "options": ["56", "63", "72", "69"], "answer": 1},
            {"text": "What is 25% of 80?", "options": ["20", "25", "16", "40"], "answer": 0},
            {"text": "What is 2 to the power of 5?", "options": ["10", "25", "32", "64"], "answer": 2},
            {"text": "How many sides does a hexagon have?", "options": ["5", "6", "7", "8"], "answer": 1},
            {"text": "What is 144 ÷ 12?", "options": ["11", "12", "13", "14"], "answer": 1},
            {"text": "What is the sum of angles in a triangle?", "options": ["90°", "180°", "270°", "360°"], "answer": 1},
            {"text": "What is 0.5 + 0.25?", "options": ["0.55", "0.7", "0.75", "0.8"], "answer": 2},
            {"text": "What is the next prime number after 7?", "options": ["9", "10", "11", "13"], "answer": 2},
            {"text": "What is the area of a square with side 6 cm?", "options": ["24 cm²", "36 cm²", "12 cm²", "30 cm²"], "answer": 1},
            {"text": "What is 1000 − 357?", "options": ["643", "653", "743", "657"], "answer": 0},
        ],
    },
    {
        "id": "web-101",
        "theme": "web",
        "title": "Web Basics",
        "description": "HTML, CSS and JavaScript fundamentals for beginners.",
        "minutes": 15,
        "questions": [
            {"text": "What does HTML stand for?", "options": ["HyperText Markup Language", "High Tech Modern Language", "Home Tool Markup Language", "Hyperlink Text Mode Language"], "answer": 0},
            {"text": "Which language is used to style web pages?", "options": ["HTML", "Python", "CSS", "SQL"], "answer": 2},
            {"text": "Which HTML tag makes a link?", "options": ["<link>", "<a>", "<href>", "<url>"], "answer": 1},
            {"text": "Which keyword declares a variable that cannot be reassigned in JavaScript?", "options": ["var", "let", "const", "static"], "answer": 2},
            {"text": "Which CSS property changes text colour?", "options": ["font-color", "text-color", "color", "foreground"], "answer": 2},
            {"text": "Which HTML tag is used for the largest heading?", "options": ["<head>", "<h6>", "<heading>", "<h1>"], "answer": 3},
            {"text": "Which HTML tag shows an image?", "options": ["<img>", "<image>", "<pic>", "<src>"], "answer": 0},
            {"text": "How do you write a comment in JavaScript (single line)?", "options": ["<!-- -->", "//", "#", "**"], "answer": 1},
            {"text": "Which CSS property sets the space inside an element's border?", "options": ["margin", "spacing", "padding", "gap"], "answer": 2},
            {"text": "Which method prints a message to the browser console?", "options": ["console.log()", "print()", "echo()", "alert.log()"], "answer": 0},
            {"text": "What does CSS stand for?", "options": ["Computer Style Sheets", "Cascading Style Sheets", "Creative Style System", "Colourful Style Sheets"], "answer": 1},
            {"text": "Which HTML element holds a numbered list?", "options": ["<ul>", "<li>", "<ol>", "<list>"], "answer": 2},
            {"text": "Which operator checks equal value AND type in JavaScript?", "options": ["=", "==", "===", "!="], "answer": 2},
            {"text": "Which CSS layout makes items sit in a flexible row or column?", "options": ["float", "flexbox", "inline", "table"], "answer": 1},
            {"text": "Which attribute gives a link its destination?", "options": ["src", "link", "href", "to"], "answer": 2},
        ],
    },
]

# SAMPLE classmates so the leaderboard is not empty in Offline Demo Mode
SAMPLE_CLASSMATES = [
    {"name": "Aarav Mehta", "average": 92, "quizzes": 7},
    {"name": "Sara Khan", "average": 88, "quizzes": 6},
    {"name": "Liam Chen", "average": 81, "quizzes": 5},
    {"name": "Diya Patel", "average": 76, "quizzes": 8},
    {"name": "Noah Fernandes", "average": 69, "quizzes": 4},
    {"name": "Ishita Rao", "average": 63, "quizzes": 5},
    {"name": "Kabir Singh", "average": 55, "quizzes": 3},
]

# Subject names used for tags and filters
TOPIC_NAMES = {"mix": "Mixed", "math": "Maths", "gk": "General Knowledge", "web": "Web & Code"}


def theme_of(quiz):
    """Which subject a quiz belongs to (math, gk, web or mix)."""
    return quiz.get("theme") or {"gk-101": "gk", "math-101": "math", "web-101": "web"}.get(quiz.get("id"), "mix")


# ---------- Reading and writing the save file ----------

def _read_all():
    try:
        return json.loads(SAVE_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}  # no file yet, or it was broken: start empty


def load(key, fallback):
    return _read_all().get(key, fallback)


def save(key, value):
    everything = _read_all()
    everything[key] = value
    SAVE_FILE.write_text(json.dumps(everything, indent=2, ensure_ascii=False), encoding="utf-8")


def remove(key):
    everything = _read_all()
    everything.pop(key, None)
    SAVE_FILE.write_text(json.dumps(everything, indent=2, ensure_ascii=False), encoding="utf-8")


# ---------- Quizzes ----------

def get_quizzes():
    """Built-in quizzes always use the latest question bank; instructor-made quizzes come from the save file."""
    saved = load("quizzes", [])
    demo_ids = {q["id"] for q in DEMO_QUIZZES}
    return DEMO_QUIZZES + [q for q in saved if q["id"] not in demo_ids]


def get_quiz(quiz_id):
    return next((q for q in get_quizzes() if q["id"] == quiz_id), None)


def save_quiz(quiz):
    saved = load("quizzes", [])
    saved.append(quiz)
    save("quizzes", saved)


# ---------- Build your own test: a subject + how many questions ----------

SECONDS_PER_QUESTION = 60   # time allowed per question in a subject test


def question_pool(subject):
    """Every question for one subject ("all" = every subject), from all its quizzes."""
    pool = []
    for quiz in get_quizzes():
        if subject == "all" or theme_of(quiz) == subject:
            pool.extend(quiz["questions"])
    return pool


def subjects_with_counts():
    """Subjects that have questions, with how many each has."""
    result = []
    for key in ("math", "gk", "web", "mix"):
        count = len(question_pool(key))
        if count:
            result.append({"key": key, "name": TOPIC_NAMES[key], "count": count})
    return result


def count_presets(maximum):
    """Quick-pick sizes for the question-count picker, never more than what is available."""
    return [n for n in (5, 10, 15, 20, 25, 30) if n < maximum] + [maximum]


def build_test(quiz_id=None, subject=None, count=None):
    """Make a test: n random questions from a subject, or (part of) one quiz.
    Returns None if there is nothing to ask."""
    import random
    if subject:
        pool = question_pool(subject)
        if not pool:
            return None
        base = {"id": "subject-" + subject, "theme": "mix" if subject == "all" else subject,
                "title": ("All Subjects" if subject == "all" else TOPIC_NAMES.get(subject, "Mixed")) + " Test",
                "per_question": SECONDS_PER_QUESTION}
    else:
        source = get_quiz(quiz_id)
        if not source:
            return None
        pool = source["questions"]
        base = {"id": source["id"], "theme": theme_of(source), "title": source["title"],
                "per_question": source["minutes"] * 60 / len(source["questions"])}
    n = min(count, len(pool)) if count and count > 0 else len(pool)
    # every question of one quiz keeps its order; a smaller pick (or a subject test) is shuffled
    questions = list(pool) if (not subject and n == len(pool)) else random.sample(pool, n)
    return {"id": base["id"], "theme": base["theme"], "title": base["title"], "subject": subject,
            "seconds": max(30, round(base["per_question"] * n)), "questions": questions}


# ---------- Accounts ----------

def get_users():
    """Demo accounts + accounts made on the Register screen.
    Names changed on the Profile screen are kept in "names" and win over the saved name."""
    names = load("names", {})
    users = []
    for u in DEMO_USERS + load("users", []):
        u = dict(u)
        if u["email"] in names:
            u["name"] = names[u["email"]]
        users.append(u)
    return users


def update_user_name(email, name):
    names = load("names", {})
    names[email] = name
    save("names", names)


def register_user(name, email, password, role):
    email = email.strip().lower()
    if any(u["email"] == email for u in get_users()):
        return False  # email already used
    saved = load("users", [])
    saved.append({"email": email, "password": password, "role": role, "name": name})
    save("users", saved)
    return True


def login(email, password, role):
    email = email.strip().lower()
    user = next((u for u in get_users()
                 if u["email"] == email and u["password"] == password and u["role"] == role), None)
    if user:
        save("current_user", {"email": user["email"], "role": user["role"], "name": user["name"]})
    return user


def logout():
    remove("current_user")


def get_current_user():
    user = load("current_user", None)
    if not user:
        return None
    # Always use the latest account name (e.g. after a name change on Profile)
    account = next((u for u in get_users() if u["email"] == user["email"]), None)
    if account:
        user["name"] = account["name"]
    return user


# ---------- Attempts (one per finished quiz) ----------

def get_all_attempts():
    return load("attempts", [])


def get_attempts(email):
    return [a for a in get_all_attempts() if a["email"] == email]


def save_attempt(attempt):
    all_attempts = get_all_attempts()
    all_attempts.append(attempt)
    save("attempts", all_attempts)


def new_id():
    return str(int(time.time() * 1000))


def now_iso():
    return datetime.now().isoformat(timespec="seconds")


def nice_date(iso_text, with_time=False):
    try:
        d = datetime.fromisoformat(iso_text.replace("Z", ""))
    except ValueError:
        return iso_text
    return d.strftime("%d/%m/%Y, %I:%M %p") if with_time else d.strftime("%d/%m/%Y")


def initials(name):
    return "".join(w[0] for w in name.split() if w)[:2].upper() or "?"


# ---------- Achievement badges (worked out from saved attempts) ----------

def _topic_of_attempt(a):
    if a.get("theme"):
        return a["theme"]
    quiz = get_quiz(a["quizId"])
    return theme_of(quiz) if quiz else "mix"


def best_streak(attempts):
    """Longest run of passed quizzes in a row (oldest to newest)."""
    best = run = 0
    for a in attempts:
        run = run + 1 if a["percent"] >= PASS_MARK else 0
        best = max(best, run)
    return best


def js_round(x):
    """Round like the website did (2.5 -> 3). Python's round() would give 2."""
    return int(math.floor(x + 0.5))


def _average(attempts):
    return sum(a["percent"] for a in attempts) / len(attempts)


BADGES = [
    {"id": "first", "icon": "1st", "name": "First Steps", "desc": "Finish your first quiz.",
     "test": lambda lst: len(lst) >= 1},
    {"id": "perfect", "icon": "100", "name": "Perfectionist", "desc": "Score 100% on any quiz.",
     "test": lambda lst: any(a["percent"] == 100 for a in lst)},
    {"id": "streak", "icon": "×3", "name": "Hat Trick", "desc": "Pass 3 quizzes in a row.",
     "test": lambda lst: best_streak(lst) >= 3},
    {"id": "explorer", "icon": "◎", "name": "Explorer", "desc": "Try Maths, General Knowledge and Web & Code.",
     "test": lambda lst: all(any(_topic_of_attempt(a) == t for a in lst) for t in ("math", "gk", "web"))},
    {"id": "flyer", "icon": "★", "name": "High Flyer", "desc": "Average 80% or more over 3+ quizzes.",
     "test": lambda lst: len(lst) >= 3 and _average(lst) >= 80},
    {"id": "master", "icon": "10", "name": "Quiz Master", "desc": "Complete 10 quizzes.",
     "test": lambda lst: len(lst) >= 10},
]


def unlocked_ids(attempts):
    return [b["id"] for b in BADGES if b["test"](attempts)]


def summarise(attempts):
    """Average score and pass rate for a list of attempts (used by the instructor)."""
    if not attempts:
        return {"average": "–", "passRate": "–"}
    passed = sum(1 for a in attempts if a["percent"] >= PASS_MARK)
    return {"average": f"{js_round(_average(attempts))}%",
            "passRate": f"{js_round(passed / len(attempts) * 100)}%"}
