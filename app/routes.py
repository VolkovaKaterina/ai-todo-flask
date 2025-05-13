from flask import Blueprint, jsonify, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.enums import TaskStatus
from app.models import User, Task
from app.forms import RegisterForm, LoginForm, TaskForm
from flask_wtf.csrf import CSRFProtect, CSRFError
from app import csrf
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OpenAI_API_KEY"))

main = Blueprint("main", __name__)

@main.route("/")
@login_required
def index():
    return render_template("index.html", user=current_user)

@main.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Email already registered", "danger")
            return redirect(url_for("main.register"))

        hashed_pw = generate_password_hash(form.password.data)
        user = User(
        name=form.name.data,
        email=form.email.data,
        password=hashed_pw
    )
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.", "success")
        return redirect(url_for("main.login"))

    return render_template("register.html", form=form)

@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Logged in successfully", "success")
            return redirect(url_for("main.index"))
        else:
            flash("Invalid email or password", "danger")

    return render_template("login.html", form=form)

@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for("main.login"))

@main.route("/todos")
@login_required
def todos():
    new_tasks = Task.query.filter_by(user_id=current_user.id, status=TaskStatus.NEW).all()
    in_progress_tasks = Task.query.filter_by(user_id=current_user.id, status=TaskStatus.IN_PROGRESS).all()
    done_tasks = Task.query.filter_by(user_id=current_user.id, status=TaskStatus.DONE).all()

    return render_template(
        "todos.html",
        new_tasks=new_tasks,
        in_progress_tasks=in_progress_tasks,
        done_tasks=done_tasks
    )

@main.route("/create", methods=["GET", "POST"])
@login_required
def create_todo():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            status=form.status.data,
            user_id=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        flash("Task created!", "success")
        return redirect(url_for("main.todos")) 

    return render_template("create_todo.html", form=form)

@main.route("/task/<int:task_id>/delete", methods=["POST"])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash("Access denied.", "danger")
        return redirect(url_for("main.todos"))

    db.session.delete(task)
    db.session.commit()
    flash("Task deleted!", "info")
    return redirect(url_for("main.todos"))

@main.route("/task/<int:task_id>/edit", methods=["POST"])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash("Access denied.", "danger")
        return redirect(url_for("main.todos"))

    task.title = request.form.get("title")
    task.description = request.form.get("description")
    task.status = request.form.get("status")
    db.session.commit()

    flash("Task updated!", "success")
    return redirect(url_for("main.todos"))

@main.route("/task/<int:task_id>/assistant", methods=["POST"])
@login_required
def task_assistant(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return jsonify({"error": "Access denied"}), 403

    prompt = f"""Act like a helpful assistant. Analyze the following task and ask a clarifying question to help the user complete it faster or better.

Task: "{task.title}"
Description: "{task.description or ''}"

Respond with one short clarifying question only.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        message = response.choices[0].message.content.strip()
        return jsonify({"question": message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@main.route("/task/<int:task_id>/assistant/reply", methods=["POST"])
@login_required
def assistant_reply(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return jsonify({"error": "Access denied"}), 403

    user_reply = request.json.get("reply", "")
    conversation_history = [
        {"role": "user", "content": f"Task: {task.title}. Description: {task.description or ''}"},
        {"role": "assistant", "content": task.assistant_notes or ""},
        {"role": "user", "content": user_reply}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )
        advice = response.choices[0].message.content.strip()
        task.assistant_notes = advice
        db.session.commit()
        return jsonify({"reply": advice})
    except Exception as e:
        return jsonify({"error": str(e)}), 500