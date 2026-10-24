"""
QuizSphere — web version made with Python + Streamlit.

RUN IT ON YOUR COMPUTER (from the frontend folder):
    pip install streamlit
    streamlit run streamlit_app.py
It opens in your browser at http://localhost:8501

PUT IT ONLINE: deploy this file on Streamlit Community Cloud (share.streamlit.io).

Demo accounts:
    Student     student@college.edu     / student123
    Instructor  instructor@college.edu  / instructor123

How it works:
  Streamlit runs this whole file from top to bottom every time you click something.
  st.session_state remembers things between those runs (who is logged in, which
  page is open, the answers so far). The page to show is st.session_state.page.

  Quizzes, accounts and scores are shared with the desktop app through data.py.
  On the internet they are saved in quizsphere_data.json on the server, which is
  reset whenever the app restarts (it is Offline Demo Mode, no database yet).
"""

import re
import time

import streamlit as st

import data
from streamlit_style import (CREDIT, CSS, TOPIC_COLORS, TROPHY, badge_coins, big_flower, esc, flower_border,
                             flower_svg, pill, score_ring)

st.set_page_config(page_title="QuizSphere", page_icon="🌸", layout="wide", initial_sidebar_state="collapsed")
st.markdown(CSS, unsafe_allow_html=True)
st.markdown(flower_border(), unsafe_allow_html=True)

LETTERS = ["A", "B", "C", "D"]
GOLD_PETAL = "#fbbf24"
ss = st.session_state
ss.setdefault("page", "home")
ss.setdefault("user", None)


# ================================================================= helpers

def go(page, **values):
    """Switch page. Used as a button's on_click, so it runs before the page is redrawn."""
    ss.page = page
    for key, value in values.items():
        ss[key] = value


def dashboard_for(user):
    return "instructor" if user and user["role"] == "instructor" else "student"


def current_user():
    """The logged-in person, with their latest name (it may have changed on Profile)."""
    if not ss.user:
        return None
    account = next((u for u in data.get_users() if u["email"] == ss.user["email"]), None)
    if account:
        ss.user["name"] = account["name"]
    return ss.user


def check_login(email, password, role):
    email = email.strip().lower()
    return next((u for u in data.get_users()
                 if u["email"] == email and u["password"] == password and u["role"] == role), None)


def eyebrow(text):
    st.markdown(f'<p class="qs-eyebrow">{esc(text)}</p>', unsafe_allow_html=True)


def html(markup):
    st.markdown(markup, unsafe_allow_html=True)


def average(attempts):
    return data.js_round(sum(a["percent"] for a in attempts) / len(attempts)) if attempts else None


# ================================================================= top bar

def navbar(user):
    if not user:
        links = [("Home", "home"), ("Log in", "login"), ("Register", "register")]
    elif user["role"] == "instructor":
        links = [("Dashboard", "instructor"), ("Create quiz", "create"), ("Leaderboard", "leaderboard"),
                 ("Profile", "profile")]
    else:
        links = [("Dashboard", "student"), ("History", "history"), ("Leaderboard", "leaderboard"),
                 ("Profile", "profile")]
    cols = st.columns([2.2] + [1.15] * len(links) + ([1] if user else []), vertical_alignment="center")
    with cols[0]:
        html(f'<div class="qs-logo">{flower_svg(30, GOLD_PETAL, 6, "#f472b6")} QuizSphere</div>')
    for col, (label, page) in zip(cols[1:], links):
        with col:
            st.button(label, key=f"nav_{page}", on_click=go, args=(page,), use_container_width=True,
                      type="primary" if ss.page == page else "tertiary")
    if user:
        with cols[-1]:
            st.button("Log out", key="nav_logout", on_click=logout, use_container_width=True)
    st.write("")



def logout():
    ss.user = None
    ss.page = "login"
    ss.pop("test", None)


def footer():
    html(f'<div class="qs-footer"><p class="credit">{CREDIT}</p>'
         f'<p class="copy">© 2026 QuizSphere · Offline Demo Mode</p></div>')


# ================================================================= pages

def page_home(user):
    left, right = st.columns([1.25, 1], vertical_alignment="center")
    with left:
        html('<div class="qs-hero"><p class="qs-eyebrow">Quiz Assessment Platform</p>'
             '<h1>Assess smarter.<br><span class="accent">Learn better.</span></h1>'
             '<p class="qs-lead">Students take timed quizzes and see instant results. Instructors create '
             'quizzes in minutes. All in one calm, simple place.</p></div>')
        b1, b2, _ = st.columns([1, 1, 1.4])
        b1.button("Get started", type="primary", use_container_width=True,
                  on_click=go, args=(dashboard_for(user) if user else "login",))
        b2.button("Create account", use_container_width=True, on_click=go, args=("register",), disabled=bool(user))
    with right:
        html(f'<div style="text-align:center">{big_flower(320)}</div>')

    st.write("")
    eyebrow("Features")
    st.markdown("## Everything you need for a quiz day")
    features = [
        ("01", "Timed quizzes", "A countdown clock keeps every attempt fair and focused."),
        ("02", "Instant results", "See your score straight away and review every answer, with balloons for great scores."),
        ("03", "Achievement badges", "Unlock badges for your first quiz, perfect scores, streaks and trying every subject."),
        ("04", "Leaderboard", "See where you rank in your class, with gold, silver and bronze for the top three."),
        ("05", "Attempt history", "Look back at every quiz you have taken and filter by subject."),
        ("06", "Easy for instructors", "Create quizzes in minutes and track attempts, average scores and pass rates."),
    ]
    for row in (features[:3], features[3:]):
        for col, (num, title, text) in zip(st.columns(3), row):
            col.markdown(f'<div class="qs-card"><span class="qs-num">{num}</span><h3>{title}</h3><p>{text}</p></div>',
                         unsafe_allow_html=True)


def role_picker(key):
    return st.segmented_control("I am a", ["Student", "Instructor"], key=key,
                                default=None if key in ss else "Student",
                                selection_mode="single") or "Student"


def page_login(user):
    _, mid, _ = st.columns([1, 1.3, 1])
    with mid, st.container(key="card_login"):
        html(pill("Offline Demo Mode", "#22d3ee"))
        st.markdown("# Welcome back")
        st.caption("Sign in to take or create quizzes.")

        def fill(role):
            u = next(x for x in data.DEMO_USERS if x["role"] == role)
            ss.login_email, ss.login_password, ss.login_role = u["email"], u["password"], role.title()

        with st.form("login_form", border=False):
            role = role_picker("login_role")
            email = st.text_input("Email address", placeholder="you@college.edu", key="login_email")
            password = st.text_input("Password", type="password", placeholder="Your password", key="login_password")
            sent = st.form_submit_button("Sign in", type="primary", use_container_width=True)
        if sent:
            if not email or not password:
                st.error("Please enter your email and password.")
            else:
                found = check_login(email, password, role.lower())
                if not found:
                    st.error("Email, password or role is not correct. Try a demo account.")
                else:
                    ss.user = {"email": found["email"], "role": found["role"], "name": found["name"]}
                    ss.page = dashboard_for(ss.user)
                    st.rerun()
        st.caption("Or fill in a demo account")
        a, b = st.columns(2)
        a.button("Demo Student", use_container_width=True, on_click=fill, args=("student",))
        b.button("Demo Instructor", use_container_width=True, on_click=fill, args=("instructor",))
        st.button("New here? Create an account", type="tertiary", on_click=go, args=("register",))


LEVEL_WORDS = ["Too short", "Weak", "Fair", "Good", "Strong"]
LEVEL_COLOURS = ["#f87171", "#f87171", "#fb923c", "#fbbf24", "#34d399"]


def password_score(pw):
    score = sum([len(pw) >= 8, bool(re.search(r"[A-Z]", pw) and re.search(r"[a-z]", pw)),
                 bool(re.search(r"[0-9]", pw)), bool(re.search(r"[^A-Za-z0-9]", pw))])
    return min(score, 1) if len(pw) < 8 else score


def page_register(user):
    _, mid, _ = st.columns([1, 1.3, 1])
    with mid, st.container(key="card_register"):
        html(pill("Offline Demo Mode", "#22d3ee"))
        st.markdown("# Create your account")
        st.caption("Demo accounts are saved on the server until the app restarts.")
        role = role_picker("reg_role")
        name = st.text_input("Full name", placeholder="e.g. Sumedha Sil")
        email = st.text_input("Email address", placeholder="you@college.edu", key="reg_email")
        password = st.text_input("Password", type="password", placeholder="At least 8 characters", key="reg_pw")
        score = password_score(password) if password else 0
        bars = "".join(f'<span style="background:{LEVEL_COLOURS[score] if password and i < max(score, 1) else "#3a3029"}">'
                       f'</span>' for i in range(4))
        html(f'<div class="qs-strength">{bars}</div>')
        st.caption(f"Strength: {LEVEL_WORDS[score]}" if password
                   else "Use 8+ characters with a capital letter, a number and a symbol.")
        confirm = st.text_input("Confirm password", type="password", placeholder="Type it again")
        if st.button("Create account", type="primary", use_container_width=True):
            if not name.strip() or not email.strip() or not password:
                st.error("Please fill in your name, email and password.")
            elif not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email.strip()):
                st.error("Please enter a valid email address.")
            elif len(password) < 8 or password_score(password) < 3:
                st.error('Please choose a stronger password (at least "Good").')
            elif password != confirm:
                st.error("The two passwords do not match.")
            elif not data.register_user(name.strip(), email, password, role.lower()):
                st.error("An account with this email already exists. Try logging in.")
            else:
                ss.user = {"email": email.strip().lower(), "role": role.lower(), "name": name.strip()}
                ss.page = dashboard_for(ss.user)
                st.rerun()
        st.button("Already have an account? Log in", type="tertiary", on_click=go, args=("login",))


def start_test(**kwargs):
    test = data.build_test(**kwargs)
    if test:
        ss.test = test
        ss.current = 0
        ss.answers = [None] * len(test["questions"])
        ss.ends_at = time.time() + test["seconds"]
        ss.test_no = ss.get("test_no", 0) + 1     # new keys for the answer buttons each test
        ss.confirm_submit = False
        ss.page = "quiz"


def page_student(user):
    attempts = data.get_attempts(user["email"])
    quizzes = data.get_quizzes()
    eyebrow("Student dashboard")
    st.markdown(f"# Welcome, {esc(user['name'])}")
    avg = average(attempts)
    a, b, c = st.columns(3)
    a.metric("Quizzes available", len(quizzes))
    b.metric("Quizzes taken", len(attempts))
    c.metric("Average score", f"{avg}%" if avg is not None else "–")

    st.markdown("## Achievement badges")
    unlocked = data.unlocked_ids(attempts)
    st.caption(f"{len(unlocked)} of {len(data.BADGES)} unlocked · hover a badge to flip it")
    html(badge_coins(data.BADGES, unlocked))

    st.write("")
    with st.container(key="card_setup"):
        eyebrow("Build your own test")
        st.markdown("### Start a test")
        st.caption("Pick a subject and how many questions you want. Questions are shuffled each time.")
        subjects = data.subjects_with_counts()
        total = sum(s["count"] for s in subjects)
        options = [("all", f"All subjects ({total})")] + [(s["key"], f'{s["name"]} ({s["count"]})') for s in subjects]
        labels = dict(options)
        subject = st.segmented_control("1 · Choose a subject", [k for k, _ in options], default="all",
                                       format_func=labels.get, key="setup_subject") or "all"
        pool = len(data.question_pool(subject))
        presets = data.count_presets(pool)
        count = st.segmented_control("2 · Number of questions", presets, default=10 if 10 in presets else presets[-1],
                                     format_func=lambda n: f"All {n}" if n == pool else str(n),
                                     key=f"setup_count_{subject}") or presets[0]
        minutes = max(1, round(count * data.SECONDS_PER_QUESTION / 60))
        name = "All subjects" if subject == "all" else data.TOPIC_NAMES[subject]
        x, y = st.columns([3, 1], vertical_alignment="center")
        x.markdown(f'<span style="color:#fbbf24;font-weight:700">{esc(name)} · {count} questions · {minutes} min</span>',
                   unsafe_allow_html=True)
        y.button("Start test", type="primary", use_container_width=True, on_click=start_test,
                 kwargs={"subject": subject, "count": count})

    st.markdown("## Available quizzes")
    for row_start in range(0, len(quizzes), 3):
        for col, quiz in zip(st.columns(3), quizzes[row_start:row_start + 3]):
            topic = data.theme_of(quiz)
            with col, st.container(key=f"card_quiz_{quiz['id']}"):
                html(pill(data.TOPIC_NAMES[topic], TOPIC_COLORS[topic]))
                st.markdown(f"### {esc(quiz['title'])}")
                st.caption(quiz["description"])
                html(pill(f"{len(quiz['questions'])} questions", "#22d3ee") + pill(f"{quiz['minutes']} min", "#22d3ee"))
                st.button("Start quiz", key=f"start_{quiz['id']}", type="primary", use_container_width=True,
                          on_click=start_test, kwargs={"quiz_id": quiz["id"]})

    st.markdown("## Recent attempts")
    st.button("See all attempts in History →", type="tertiary", on_click=go, args=("history",))
    if not attempts:
        st.caption("No attempts yet. Pick a quiz above to begin.")
    for a in reversed(attempts[-5:]):
        attempt_row(a, key="recent")


def attempt_row(a, key):
    passed = a["percent"] >= data.PASS_MARK
    topic = data._topic_of_attempt(a)
    with st.container(key=f"card_{key}_{a['id']}"):
        left, mid, right = st.columns([4, 1.2, 1.4], vertical_alignment="center")
        left.markdown(f'{pill(data.TOPIC_NAMES.get(topic, "Mixed"), TOPIC_COLORS.get(topic, "#93b4ff"))}'
                      f'<div style="font-weight:700;font-size:1.1rem;margin-top:.3rem">{esc(a["quizTitle"])}</div>'
                      f'<div class="qs-muted" style="font-size:.85rem">{data.nice_date(a["date"], True)} · '
                      f'{a["correct"]}/{a["total"]} correct</div>', unsafe_allow_html=True)
        mid.markdown(f'<div class="qs-score">{a["percent"]}%</div>'
                     f'<div class="{"qs-pass" if passed else "qs-fail"}">{"Passed" if passed else "Not passed"}</div>',
                     unsafe_allow_html=True)
        right.button("View result", key=f"view_{key}_{a['id']}", use_container_width=True,
                     on_click=go, args=("results",), kwargs={"result_id": a["id"], "result_new": False})


# ---------------------------------------------------------------- taking a test

def finish_test():
    test, answers = ss.test, ss.answers
    questions = test["questions"]
    correct = sum(1 for q, a in zip(questions, answers) if a == q["answer"])
    user = current_user()
    before = data.unlocked_ids(data.get_attempts(user["email"]))
    attempt = {
        "id": data.new_id(), "email": user["email"], "quizId": test["id"], "quizTitle": test["title"],
        "answers": answers, "correct": correct, "total": len(questions),
        "percent": data.js_round(correct / len(questions) * 100), "date": data.now_iso(),
        "theme": test["theme"], "subject": test["subject"], "questions": questions,
    }
    data.save_attempt(attempt)
    after = data.unlocked_ids(data.get_attempts(user["email"]))
    ss.fresh_badges = [b for b in after if b not in before]
    ss.pop("test", None)
    ss.confirm_submit = False
    ss.page, ss.result_id, ss.result_new = "results", attempt["id"], True


def ask_submit(on):
    ss.confirm_submit = on


@st.fragment(run_every=1)
def countdown():
    """Re-draws only the clock once a second. At 0 the test is handed in automatically."""
    if "test" not in ss:
        return
    left = max(0, int(ss.ends_at - time.time()))
    total = ss.test["seconds"]
    colour = "#f87171" if left <= 30 else "#fbbf24"
    st.markdown(f'<div style="text-align:right"><span style="font-size:2.2rem;font-weight:800;color:{colour}">'
                f'{left // 60:02d}:{left % 60:02d}</span><br><span class="qs-muted">Time left</span></div>',
                unsafe_allow_html=True)
    st.progress(left / total)
    if left <= 0:
        finish_test()
        st.rerun(scope="app")


def set_current(i):
    ss.current = i


def page_quiz(user):
    if "test" not in ss:
        go(dashboard_for(user))
        st.rerun()
    test = ss.test
    questions = test["questions"]
    i = ss.current
    head, clock = st.columns([3, 1.3], vertical_alignment="bottom")
    with head:
        eyebrow(data.TOPIC_NAMES.get(test["theme"], "Mixed"))
        st.markdown(f"# {esc(test['title'])}")
    with clock:
        countdown()
    answered = sum(a is not None for a in ss.answers)
    st.caption(f"Answered {answered} of {len(questions)}")
    st.progress(answered / len(questions))

    main, side = st.columns([2.6, 1])
    with main, st.container(key="card_question"):
        q = questions[i]
        html(f'<p style="color:#fbbf24;font-weight:700;margin:0">Question {i + 1} of {len(questions)}</p>')
        st.markdown(f"### {esc(q['text'])}")
        key = f"ans_{ss.test_no}_{i}"
        if key not in ss and ss.answers[i] is not None:
            ss[key] = ss.answers[i]          # bring back the answer chosen earlier

        def pick(index=i, k=key):
            ss.answers[index] = ss[k]
        st.radio("Choose one answer", [0, 1, 2, 3], key=key, on_change=pick, index=None,
                 format_func=lambda n, opts=q["options"]: f"{LETTERS[n]}.   {opts[n]}", label_visibility="collapsed")
        p, _, n = st.columns([1, 2, 1])
        p.button("← Previous", use_container_width=True, disabled=i == 0, on_click=set_current, args=(i - 1,))
        n.button("Next →", use_container_width=True, disabled=i == len(questions) - 1,
                 on_click=set_current, args=(i + 1,))
    with side, st.container(key="card_palette"):
        st.markdown("**Questions**")
        per_row = 5
        for start in range(0, len(questions), per_row):
            for col, j in zip(st.columns(per_row, gap="small"), range(start, min(start + per_row, len(questions)))):
                done = ss.answers[j] is not None
                col.button(f"{j + 1}", key=f"pal_{j}", use_container_width=True, on_click=set_current, args=(j,),
                           type="primary" if j == i else ("secondary" if not done else "tertiary"),
                           help="Answered" if done else "Not answered yet")
        st.caption("Gold = this question · plain number = answered")
        if not ss.get("confirm_submit"):
            st.button("Submit quiz", type="primary", use_container_width=True, on_click=ask_submit, args=(True,))
        else:
            # Ask before handing in: answers can't be changed afterwards
            left = sum(a is None for a in ss.answers)
            st.warning(f"You have {left} unanswered question(s). You cannot change answers after submitting."
                       if left else "All questions answered. You cannot change answers after submitting.")
            st.button("Yes, submit", type="primary", use_container_width=True, on_click=finish_test)
            st.button("Keep going", use_container_width=True, on_click=ask_submit, args=(False,))


# ---------------------------------------------------------------- results

def page_results(user):
    mine = data.get_attempts(user["email"])
    attempt = next((a for a in mine if a["id"] == ss.get("result_id")), None)
    if not attempt:
        go(dashboard_for(user))
        st.rerun()
    questions = attempt.get("questions") or (data.get_quiz(attempt["quizId"]) or {}).get("questions", [])
    passed = attempt["percent"] >= data.PASS_MARK
    fresh = ss.get("fresh_badges", []) if ss.get("result_new") else []
    if ss.get("result_new"):
        if attempt["percent"] >= 80:
            st.balloons()          # celebrate great scores
        ss.result_new = False      # only celebrate once

    with st.container(key="card_result"):
        ring, words = st.columns([1, 3], vertical_alignment="center")
        ring.markdown(score_ring(attempt["percent"], passed), unsafe_allow_html=True)
        with words:
            html(f'<span class="{"qs-pass" if passed else "qs-fail"}">{"Passed" if passed else "Not passed"}</span>')
            st.markdown(f"# {esc(attempt['quizTitle'])}")
            st.write(f"You answered {attempt['correct']} out of {attempt['total']} questions correctly. "
                     f"Pass mark is {data.PASS_MARK}%.")
            b1, b2, _ = st.columns([1.3, 1, 1.5])
            b1.button("Back to dashboard", type="primary", use_container_width=True, on_click=go,
                      args=(dashboard_for(user),))
            retry = ({"subject": attempt["subject"], "count": attempt["total"]} if attempt.get("subject")
                     else {"quiz_id": attempt["quizId"], "count": attempt["total"]})
            b2.button("Try again", use_container_width=True, on_click=start_test, kwargs=retry)

    if attempt["percent"] == 100:
        with st.container(key="card_trophy"):
            t, w = st.columns([1, 3], vertical_alignment="center")
            t.markdown(f'<div style="text-align:center">{TROPHY}</div>', unsafe_allow_html=True)
            with w:
                eyebrow("Perfect score")
                st.markdown("## You earned the gold trophy!")
                st.write("Every single answer was correct. Brilliant work.")

    eyebrow("New achievement" if fresh else "Badge showcase")
    st.markdown("## " + (("Badge unlocked!" if len(fresh) == 1 else f"{len(fresh)} badges unlocked!") if fresh
                         else "Your badges"))
    unlocked = data.unlocked_ids(mine)
    st.caption(f"{len(unlocked)} of {len(data.BADGES)} badges unlocked")
    html(badge_coins(data.BADGES, unlocked, fresh))

    st.markdown("## Review your answers")
    for n, q in enumerate(questions):
        chosen = attempt["answers"][n] if n < len(attempt["answers"]) else None
        right = chosen == q["answer"]
        mark = '<span class="qs-pass">✓ Correct</span>' if right else '<span class="qs-fail">✗ Incorrect</span>'
        mine_text = "Not answered" if chosen is None else q["options"][chosen]
        html(f'<div class="qs-card {"" if right else "qs-wrong"}"><div class="qs-row"><b>{n + 1}. {esc(q["text"])}</b>'
             f'{mark}</div><p>Your answer: {esc(mine_text)}</p><p>Correct answer: {esc(q["options"][q["answer"]])}</p></div>')


# ---------------------------------------------------------------- history, leaderboard, profile

def page_history(user):
    eyebrow("Student")
    st.markdown("# Attempt history")
    attempts = list(reversed(data.get_attempts(user["email"])))
    keys = ["all", "math", "gk", "web", "mix"]
    names = {"all": "All", **data.TOPIC_NAMES}
    topic = st.segmented_control("Filter by subject", keys, default="all", format_func=names.get,
                                 key="hist_filter", label_visibility="collapsed") or "all"
    shown = [a for a in attempts if topic == "all" or data._topic_of_attempt(a) == topic]
    st.caption(f"Showing {len(shown)} of {len(attempts)} attempt(s)")
    if not shown:
        st.caption("No attempts for this subject yet.")
    for a in shown:
        attempt_row(a, key="hist")


def page_leaderboard(user):
    eyebrow("Class rankings")
    st.markdown("# Leaderboard")
    st.caption('Ranked by average score. Names marked "sample" are demo classmates.')
    by_email = {}
    for a in data.get_all_attempts():
        by_email.setdefault(a["email"], []).append(a["percent"])
    users = data.get_users()
    people = []
    for email, scores in by_email.items():
        account = next((u for u in users if u["email"] == email), None)
        people.append({"name": account["name"] if account else email, "average": data.js_round(sum(scores) / len(scores)),
                       "quizzes": len(scores), "me": email == user["email"]})
    if user["role"] == "student" and user["email"] not in by_email:
        people.append({"name": user["name"], "average": 0, "quizzes": 0, "me": True})
    people += [dict(c, sample=True) for c in data.SAMPLE_CLASSMATES]
    people.sort(key=lambda p: (-p["average"], -p["quizzes"]))

    def tags(p):
        return ('<span class="qs-tag you">You</span>' if p.get("me") else "") + \
               ('<span class="qs-tag">sample</span>' if p.get("sample") else "")

    medals = {1: ("#fbbf24", 150), 2: ("#e5e7eb", 110), 3: ("#f59e0b", 80)}
    spots = []
    for rank in (2, 1, 3):
        if rank <= len(people):
            p = people[rank - 1]
            colour, height = medals[rank]
            spots.append(f'<div class="qs-spot"><div class="qs-avatar" style="background:{colour}">'
                         f'{esc(data.initials(p["name"]))}</div><b>{esc(p["name"])}</b>{tags(p)}'
                         f'<div style="color:{colour};font-weight:800;font-size:1.3rem">{p["average"]}%</div>'
                         f'<div class="qs-block {"qs-me" if p.get("me") else ""}" style="height:{height}px;color:{colour}">'
                         f'{rank}</div></div>')
    st.markdown("### Top three students")
    html(f'<div class="qs-podium">{"".join(spots)}</div>')
    st.markdown("### Everyone else")
    for n, p in enumerate(people[3:], start=4):
        note = "Take a quiz to join the ranking" if p["quizzes"] == 0 else f'{p["quizzes"]} quiz(zes)'
        html(f'<div class="qs-card {"qs-me" if p.get("me") else ""}"><div class="qs-row">'
             f'<span class="qs-score" style="font-size:1.2rem;width:3rem">#{n}</span>'
             f'<div style="flex:1"><b>{esc(p["name"])}</b>{tags(p)}<div class="qs-muted" style="font-size:.8rem">{note}</div>'
             f'<div class="qs-meter"><span style="width:{p["average"]}%"></span></div></div>'
             f'<span style="font-weight:800;font-size:1.2rem">{p["average"]}%</span></div></div>')


def page_profile(user):
    _, mid, _ = st.columns([1, 1.3, 1])
    with mid, st.container(key="card_profile"):
        name_now = ss.get("profile_name", user["name"])
        html(f'<div style="text-align:center"><div class="qs-avatar" style="background:#fbbf24;width:90px;height:90px;'
             f'font-size:2rem">{esc(data.initials(name_now.strip() or "?"))}</div></div>')
        st.markdown("<h1 style='text-align:center'>Your profile</h1>", unsafe_allow_html=True)
        html(f'<div style="text-align:center">{pill(user["role"].title(), "#22d3ee")}</div>')
        st.caption("Email")
        st.write(user["email"])
        new_name = st.text_input("Display name", value=user["name"], key="profile_name")
        if st.button("Save name", type="primary", use_container_width=True):
            clean = " ".join(new_name.split())
            if len(clean) < 2:
                st.error("Please enter a name with at least 2 characters.")
            else:
                data.update_user_name(user["email"], clean)
                st.success(f'Saved! Your dashboard and the leaderboard will now show "{clean}".')


# ---------------------------------------------------------------- instructor

def page_instructor(user):
    quizzes = data.get_quizzes()
    attempts = data.get_all_attempts()
    overall = data.summarise(attempts)
    head, button = st.columns([3, 1], vertical_alignment="bottom")
    with head:
        eyebrow("Instructor dashboard")
        st.markdown(f"# Welcome, {esc(user['name'])}")
    button.button("+ Create quiz", type="primary", use_container_width=True, on_click=go, args=("create",))
    a, b, c, d = st.columns(4)
    a.metric("Total quizzes", len(quizzes))
    b.metric("Total attempts", len(attempts))
    c.metric("Average score", overall["average"])
    d.metric("Pass rate", overall["passRate"])
    st.markdown("## Quizzes and participation")
    st.caption("Each quiz with number of attempts, average score and pass rate")
    rows = []
    for quiz in quizzes:
        mine = [x for x in attempts if x["quizId"] == quiz["id"]]
        s = data.summarise(mine)
        topic = data.theme_of(quiz)
        rows.append(f'<tr><td><b>{esc(quiz["title"])}</b></td><td style="color:{TOPIC_COLORS[topic]}">'
                    f'{data.TOPIC_NAMES[topic]}</td><td>{len(quiz["questions"])}</td><td>{quiz["minutes"]} min</td>'
                    f'<td>{len(mine)}</td><td>{s["average"]}</td><td>{s["passRate"]}</td></tr>')
    html('<table class="qs-table"><tr><th>Quiz</th><th>Subject</th><th>Questions</th><th>Time</th><th>Attempts</th>'
         f'<th>Average</th><th>Pass rate</th></tr>{"".join(rows)}</table>')


def page_create(user):
    eyebrow("Instructor")
    st.markdown("# Create a new quiz")
    ss.setdefault("cq_blocks", [0])
    ss.setdefault("cq_next", 1)
    subjects = {"math": "Maths", "gk": "General Knowledge", "web": "Web & Code", "mix": "Mixed"}
    with st.container(key="card_details"):
        st.markdown("### Quiz details")
        title = st.text_input("Quiz title", placeholder="e.g. Science Basics", key="cq_title")
        desc = st.text_input("Short description", placeholder="What is this quiz about?", key="cq_desc")
        a, b = st.columns(2)
        with a:
            topic = st.segmented_control("Subject", list(subjects), format_func=subjects.get, key="cq_topic",
                                         default=None if "cq_topic" in ss else "math") or "math"
        minutes = b.number_input("Time limit (minutes)", min_value=1, max_value=180, value=10, key="cq_minutes")

    def add_block():
        ss.cq_blocks.append(ss.cq_next)
        ss.cq_next += 1

    def remove_block(block_id):
        if len(ss.cq_blocks) == 1:
            ss.cq_error = "A quiz needs at least one question."
        else:
            ss.cq_blocks.remove(block_id)

    for number, block_id in enumerate(ss.cq_blocks, start=1):
        with st.container(key=f"card_q_{block_id}"):
            st.markdown(f"### Question {number}")
            st.text_input("Question text", key=f"cq_{block_id}_text")
            st.caption("Type the 4 answer choices and select the correct one.")
            o1, o2 = st.columns(2)
            for k in range(4):
                (o1 if k % 2 == 0 else o2).text_input(f"Option {LETTERS[k]}", key=f"cq_{block_id}_o{k}")
            st.radio("Correct answer", [0, 1, 2, 3], format_func=LETTERS.__getitem__, horizontal=True,
                     key=f"cq_{block_id}_ans")
            st.button("Remove question", key=f"rm_{block_id}", on_click=remove_block, args=(block_id,))

    left, right = st.columns(2)
    left.button("+ Add question", use_container_width=True, on_click=add_block)
    if right.button("Save quiz", type="primary", use_container_width=True):
        ss.cq_error = None
        questions = []
        for number, block_id in enumerate(ss.cq_blocks, start=1):
            text = ss.get(f"cq_{block_id}_text", "").strip()
            opts = [ss.get(f"cq_{block_id}_o{k}", "").strip() for k in range(4)]
            if not text or not all(opts):
                ss.cq_error = f"Question {number} needs its text and all 4 options filled in."
                break
            questions.append({"text": text, "options": opts, "answer": ss.get(f"cq_{block_id}_ans", 0)})
        if not title.strip():
            ss.cq_error = "Please give the quiz a title."
        if not ss.cq_error:
            data.save_quiz({"id": "quiz-" + data.new_id(), "title": title.strip(), "theme": topic,
                            "description": desc.strip() or f"A quiz created by {user['name']}.",
                            "minutes": int(minutes), "questions": questions})
            for key in [k for k in ss.keys() if str(k).startswith("cq_")]:
                del ss[key]
            go("instructor")
            st.rerun()
    if ss.get("cq_error"):
        st.error(ss.cq_error)


# ================================================================= which page to show

PAGES = {
    "home": (page_home, None), "login": (page_login, None), "register": (page_register, None),
    "student": (page_student, "student"), "instructor": (page_instructor, "instructor"),
    "quiz": (page_quiz, "user"), "results": (page_results, "user"), "history": (page_history, "student"),
    "leaderboard": (page_leaderboard, "user"), "profile": (page_profile, "user"), "create": (page_create, "instructor"),
}

user = current_user()
page_fn, guard = PAGES.get(ss.page, PAGES["home"])
if guard and not user:                                   # must log in first
    ss.page, page_fn = "login", page_login
elif guard in ("student", "instructor") and user["role"] != guard:
    ss.page = dashboard_for(user)                        # wrong role: go to your own dashboard
    page_fn = PAGES[ss.page][0]

navbar(user)
page_fn(user)
footer()
