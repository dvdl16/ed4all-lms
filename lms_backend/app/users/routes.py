from flask import jsonify
from lms_backend.app.models import User
from lms_backend.app.db import db
from lms_backend.app.auth import basic_auth
from pydantic import BaseModel, EmailStr
from enum import Enum
from werkzeug.security import generate_password_hash
from flask_openapi3 import Tag, APIBlueprint
from lms_backend.app.utils import to_dict

# Set tags for use in OpenAPI Swagger documentation
auth_tag = Tag(name="auth", description="Authentication")

# Set Flask Blueprint
auth_bp = APIBlueprint("auth", __name__, url_prefix="/auth")


# Pydantic models for validation
class RoleEnum(str, Enum):
    learner = "Learner"
    teacher = "Teacher"


class CurriculumEnum(str, Enum):
    caps = "CAPS"
    ng = "NG"
    cbc = "CBC"
    cbc_knec = "CBC_KNEC"
    intl = "INTL"


class UserCreateSchema(BaseModel):
    email: EmailStr
    name: str
    surname: str
    password: str
    grade: str
    country: str
    curriculum: CurriculumEnum
    role: RoleEnum


class UserResponseSchema(BaseModel):
    email: EmailStr
    name: str
    surname: str
    grade: str
    country: str
    curriculum: CurriculumEnum
    role: RoleEnum


# Endpoints
@auth_bp.post("/users", tags=[auth_tag], responses={200: UserResponseSchema, 409: {}})
@basic_auth.login_required
def create_user(body: UserCreateSchema) -> UserResponseSchema:
    """
    Create a new user
    """
    # Check if user already exists
    if User.query.filter_by(email=body.email).first():
        return jsonify({"message": "User with this email already exists"}), 409

    # Create new user
    user = User(
        email=body.email,
        name=body.name,
        surname=body.surname,
        password_hash=generate_password_hash(body.password),
        grade=body.grade,
        country=body.country,
        curriculum=body.curriculum,
        role=body.role,
    )
    db.session.add(user)
    db.session.commit()
    response_instance = UserResponseSchema(**to_dict(user, User))
    return jsonify(response_instance.model_dump()), 201


@auth_bp.get("/users", tags=[auth_tag])
@basic_auth.login_required
def get_users():
    """
    Get all users
    """
    users = User.query.all()

    response_instances = [UserResponseSchema(**to_dict(user, User)) for user in users]
    return jsonify([instance.model_dump() for instance in response_instances]), 200
