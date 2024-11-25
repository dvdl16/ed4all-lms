from lms_backend.app.config import Config
from lms_backend.app.db import db
from lms_backend.app.models import Course, User
import uuid

from werkzeug.security import generate_password_hash


def create_demo_user(config: Config):
    """
    Creates a user in the database
    """
    # Check if user already exists
    email = config.DEMO_USER_NAME
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return

    # Create new user
    user = User(
        email=email,
        name="Demo",
        surname="User",
        password_hash=generate_password_hash(config.DEMO_USER_PASS),
        grade=10,
        country="ZA",
        curriculum="CAPS",
        role="Teacher",
    )
    db.session.add(user)
    db.session.commit()


def create_standard_courses():
    """
    Creates default courses in the database
    """
    standard_courses = ["maths", "science", "physics", "chemistry"]

    # Check if course already exists
    for course_name in standard_courses:
        existing_course = Course.query.filter_by(name=course_name).first()

        if existing_course:
            return

        # Create new course
        course = Course(name=course_name)
        db.session.add(course)
        db.session.commit()


def to_dict(object, model):
    """
    Serialise an SQLAlchemy object
    """
    return {
        column.name: getattr(object, column.name) for column in model.__table__.columns
    }


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False
