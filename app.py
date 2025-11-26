from flask import Flask, render_template, redirect, url_for, request, flash, session
from config import Config
from models import init_db, SessionLocal, User, Note, Task
from forms import RegisterForm, LoginForm, NoteForm, TaskForm
from werkzeug.security import generate_password_hash, check_password_hash
import requests

app = Flask(__name__)
app.config.from_object(Config)
init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- simple session-based auth (not production)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db = next(get_db())
        existing = db.query(User).filter_by(username=form.username.data).first()
        if existing:
            flash("Username taken", "warning")
            return redirect(url_for("register"))
        u = User(username=form.username.data)
        u.set_password(form.password.data)
        db.add(u)
        db.commit()
        flash("Account created — please login", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db = next(get_db())
        u = db.query(User).filter_by(username=form.username.data).first()
        if u and u.check_password(form.password.data):
            session["user_id"] = u.id
            session["username"] = u.username
            flash("Logged in", "success")
            return redirect(url_for("dashboard"))
        flash("Invalid credentials", "danger")
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out", "info")
    return redirect(url_for("index"))

def require_login():
    if not session.get("user_id"):
        flash("Please login", "warning")
        return False
    return True

@app.route("/dashboard")
def dashboard():
    if not require_login():
        return redirect(url_for("login"))
    # basic weather placeholder: user can replace with real API keys; shows how integration would work
    weather = None
    try:
        # Open-Meteo public API example (no key) — returns weather for a fixed lat/lon (example: New Delhi)
        r = requests.get("https://api.open-meteo.com/v1/forecast?latitude=28.6139&longitude=77.2090&current_weather=true")
        if r.ok:
            data = r.json()
            weather = data.get("current_weather", {})
    except Exception:
        weather = None

    return render_template("dashboard.html", weather=weather)

# Notes
@app.route("/notes", methods=["GET","POST"])
def notes():
    if not require_login():
        return redirect(url_for("login"))
    form = NoteForm()
    db = next(get_db())
    uid = session["user_id"]
    if form.validate_on_submit():
        n = Note(user_id=uid, title=form.title.data, body=form.body.data)
        db.add(n)
        db.commit()
        flash("Note saved", "success")
        return redirect(url_for("notes"))
    notes = db.query(Note).filter_by(user_id=uid).all()
    return render_template("notes.html", notes=notes, form=form)

@app.route("/delete_note/<int:nid>", methods=["POST"])
def delete_note(nid):
    db = next(get_db())
    n = db.query(Note).filter_by(id=nid, user_id=session.get("user_id")).first()
    if n:
        db.delete(n)
        db.commit()
        flash("Deleted", "info")
    return redirect(url_for("notes"))

# Tasks
@app.route("/tasks", methods=["GET","POST"])
def tasks():
    if not require_login():
        return redirect(url_for("login"))
    form = TaskForm()
    db = next(get_db())
    uid = session["user_id"]
    if form.validate_on_submit():
        t = Task(user_id=uid, title=form.title.data, done=0)
        db.add(t)
        db.commit()
        flash("Task added", "success")
        return redirect(url_for("tasks"))
    if request.method == "POST" and request.form.get("toggle"):
        tid = int(request.form.get("toggle"))
        t = db.query(Task).filter_by(id=tid, user_id=uid).first()
        if t:
            t.done = 0 if t.done else 1
            db.commit()
            flash("Task updated", "info")
        return redirect(url_for("tasks"))
    tasks = db.query(Task).filter_by(user_id=uid).all()
    return render_template("tasks.html", tasks=tasks, form=form)

@app.route("/delete_task/<int:tid>", methods=["POST"])
def delete_task(tid):
    db = next(get_db())
    t = db.query(Task).filter_by(id=tid, user_id=session.get("user_id")).first()
    if t:
        db.delete(t)
        db.commit()
        flash("Task removed", "info")
    return redirect(url_for("tasks"))

# Simple calculator route (client-side) and timer is handled in front-end JS
if __name__ == "__main__":
    app.run(debug=True)
