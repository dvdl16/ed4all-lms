from flask import jsonify
from pydantic import BaseModel
from sqlalchemy import and_
from lms_backend.app.models import Course, User, UserCourse
from lms_backend.app.db import db
from flask_openapi3 import Tag, APIBlueprint
from lms_backend.app.auth import basic_auth

from lms_backend.app.utils import to_dict

# Set tags for use in OpenAPI Swagger documentation
courses_tag = Tag(name="courses", description="Course Assignments")

# Set Flask Blueprint
courses_bp = APIBlueprint("courses", __name__)


# Pydantic models for validation
class AssignmentCreateSchema(BaseModel):
    user_id: int
    course_id: int


class AssignmentResponseSchema(BaseModel):
    id: int
    user_id: int
    course_id: int


@courses_bp.post(
    "/assignments",
    tags=[courses_tag],
    responses={200: AssignmentResponseSchema, 409: {}},
)
@basic_auth.login_required
def assign_course(body: AssignmentCreateSchema):
    """
    Assign course to user
    """
    # Check if assignment already exists
    if UserCourse.query.filter(
        and_(UserCourse.user_id == body.user_id, UserCourse.course_id == body.course_id)
    ).first():
        return jsonify({"message": "User-Course Assignment already exists"}), 409

    # Check if user exists
    if not User.query.filter_by(id=body.user_id).first():
        return jsonify({"message": "User with this id does not exist"}), 400

    # Check if course exists
    if not Course.query.filter_by(id=body.course_id).first():
        return jsonify({"message": "Course with this id does not exist"}), 400

    user_course = UserCourse(user_id=body.user_id, course_id=body.course_id)
    db.session.add(user_course)
    db.session.commit()

    response_instance = AssignmentResponseSchema(**to_dict(user_course, UserCourse))
    return jsonify(response_instance.model_dump()), 201
