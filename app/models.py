from app import db
from flask_login import UserMixin
from sqlalchemy import Enum
from .enums import TaskStatus

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) 
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    assistant_notes = db.Column(db.Text)
    status = db.Column(
        Enum(TaskStatus, name="task_status_enum"),
        nullable=False,
        default=TaskStatus.NEW
    )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('tasks', lazy=True))    
