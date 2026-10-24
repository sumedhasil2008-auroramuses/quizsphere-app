# QuizSphere — Frontend (Python only)

**Front-end developer:** Sumedha Sil · SRM KTR · CSE Core · RA2611003011378

The QuizSphere frontend is written only in **Python**. It comes in two versions
that share the same quizzes, accounts, badges and scores (`data.py`):

| Version | Main file | Opens as | Can be put online? |
|---|---|---|---|
| **Web app** (Streamlit) | `streamlit_app.py` | a page in your browser | Yes, on Streamlit Community Cloud |
| **Desktop app** (Tkinter) | `main.py` | a window on your computer | No, it runs on your own computer only |

Demo accounts: **Student** `student@college.edu` / `student123` · **Instructor** `instructor@college.edu` / `instructor123`

It runs in **Offline Demo Mode**: there's no database yet. Data is kept in `quizsphere_data.json`.

---

## 1. Web app (Streamlit)

### See it on your computer
In the VS Code terminal, from the `frontend` folder:

```
pip install streamlit
streamlit run streamlit_app.py
```

Your browser opens at http://localhost:8501. Press `Ctrl + C` in the terminal to stop it.

### Put it online (Streamlit Community Cloud, free)
1. Go to https://share.streamlit.io and sign in with GitHub.
2. Click **Create app → Deploy a public app from GitHub**.
3. Fill in:
   - **Repository:** `manavtarashnayak/quiz-assessment-platform`
   - **Branch:** `feature/frontend` (or `main` once it is merged)
   - **Main file path:** `frontend/streamlit_app.py`
4. Click **Deploy**. The first build takes a few minutes. Streamlit installs what is listed in
   `frontend/requirements.txt` (just `streamlit`), not the backend's packages.

Online, the demo data is shared by everyone using the link, and it resets whenever the app restarts.

## 2. Desktop app (Tkinter)

Open `main.py` in VS Code and click **▶ Run Python File**, or run:

```
python main.py
```

Tkinter apps open a window on your computer, so they **can't** be deployed to Vercel or Streamlit.

---

## Which file does what

| File | What it does |
|---|---|
| `data.py` | Quizzes (45 questions), accounts, scores, badges, "Start a test" builder. Shared by both apps |
| `streamlit_app.py` | The web app: every page (home, login, register, dashboards, quiz, results, history, leaderboard, profile, create quiz) |
| `streamlit_style.py` | The web app's look: colours, flower border, score ring, trophy, badge coins |
| `requirements.txt` | Tells Streamlit Cloud to install `streamlit` |
| `main.py` | Starts the desktop app and switches between its pages |
| `theme.py`, `effects.py`, `border.py`, `background.py` | Desktop app look: colours, animations, flower border |
| `screens/*.py` | One file per desktop screen (not called `pages`, because Streamlit would treat a `pages` folder as web pages) |
