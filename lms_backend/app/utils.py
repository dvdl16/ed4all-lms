from lms_backend.app.config import Config
from lms_backend.app.db import db
from lms_backend.app.models import User

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


def to_dict(object, model):
    """
    Serialise an SQLAlchemy object
    """
    return {
        column.name: getattr(object, column.name) for column in model.__table__.columns
    }
