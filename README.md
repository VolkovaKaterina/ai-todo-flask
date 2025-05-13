# AI ToDo App

AI-powered ToDo web app built with **Flask**, **SQLAlchemy**, **Flask-Login**, **Bulma** CSS, and **OpenAI Assistant** integration.

---

## Features

* Register / Login
* Create / Edit / Delete tasks
* Tasks grouped by status: New, In Progress, Done
* AI Assistant gives smart suggestions for tasks
* Assistant conversation support (basic)
* CSRF protection
* SQLite + Alembic migrations
* Responsive Bulma layout

---

## Installation

### 1. Clone the project

```bash
git clone  https://github.com/VolkovaKaterina/ai-todo-flask.git
cd ai-todo
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment setup

Create a `.env` file in the project root:

```
SECRET_KEY=your-secret-key
OPENAI_API_KEY=sk-xxx-your-openai-key
```

Make sure to set your [OpenAI API key](https://platform.openai.com/account/api-keys).

---

## Database setup

### Initialize DB and migrations:

```bash
flask db init
```

### Generate migration for models

```bash
flask db migrate -m "Initial migration"
```

### Apply migrations

```bash
flask db upgrade
```

---

## Run the app

```bash
flask run
```

Visit [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🧪 Useful commands

| Task                 | Command                     |
| -------------------- | --------------------------- |
| Create new migration | `flask db migrate -m "msg"` |
| Apply migrations     | `flask db upgrade`          |
| Rollback migration   | `flask db downgrade`        |
| Start server         | `flask run`                 |

---

---

## Assistant logic

Uses `openai.ChatCompletion` to:

* Analyze task title/description
* Ask clarifying question
* Allow user to respond
* Save final assistant note in DB

---

## Security

* CSRF protection via Flask-WTF
* Passwords hashed with Werkzeug
* Routes protected with `@login_required`

---

## UI Framework

* [Bulma CSS](https://bulma.io/) for layout
* Modals for edit / assistant
* Responsive and mobile-ready

---

## Future improvements

* True AI Agent integration (tool calls)
* Search integration (Google, Skyscanner)
* Chat history per task
* Drag-and-drop Kanban UI

---

