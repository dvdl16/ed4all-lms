from lms_backend.app.db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    password_hash = db.Column(db.String(128), nullable=False)
    grade = db.Column(db.Integer)
    country = db.Column(db.String(50))
    curriculum = db.Column(db.String(50))
    siyavula_account_id = db.Column(db.String(50))
    role = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class UserCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    assigned_at = db.Column(db.DateTime, default=db.func.current_timestamp())
