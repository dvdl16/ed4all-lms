from typing import Any, Dict
from uuid import UUID
from flask import Response, jsonify
from flask_openapi3 import Tag, APIBlueprint
from pydantic import BaseModel
from lms_backend.app.auth import basic_auth
from lms_backend.app.models import User
from lms_backend.app.siyavula.services import SiyavulaUserAPI, depends_on_siyavula_api
from flask import g

# Set tags for use in OpenAPI Swagger documentation
siyavula_tag = Tag(name="siyavula", description="Siyavula API")

# Set Flask Blueprint
siyavula_bp = APIBlueprint("siyavula", __name__, url_prefix="/siyavula")


# Pydantic models
class SiyavulaActivity(BaseModel):
    id: UUID
    sequence_id: UUID
    retry_url: str
    next_url: str


class SiyavulaResponse(BaseModel):
    id: UUID
    complete: bool
    question_html: str
    random_seed: int
    template_id: int


class SiyavulaModel(BaseModel):
    activity: SiyavulaActivity
    response: SiyavulaResponse
    meta: Any


class SiyavulaCreateModel(BaseModel):
    user_id: int
    activity_uuid: UUID
    response_uuid: UUID


class SiyavulaCreateAnswersModel(SiyavulaCreateModel):
    answers: Dict[str, str]


class SiyavulaPracticeRequest(BaseModel):
    section_id: int
    user_id: int


@siyavula_bp.post("/activity", tags=[siyavula_tag], responses={200: SiyavulaModel})
@basic_auth.login_required
@depends_on_siyavula_api
def create_activity(body: SiyavulaPracticeRequest):
    """
    Create a practice activity
    """
    # Check if user exists
    if not User.query.filter_by(id=body.user_id).first():
        return jsonify({"message": "User with this id does not exist"}), 400

    api = SiyavulaUserAPI(client_token=g.siavula_api.client_token, user_id=body.user_id)

    siyavula_response = api.create_practice_activity(section_id=body.section_id)

    flask_response = Response(
        siyavula_response.content,
        status=siyavula_response.status_code,
        content_type=siyavula_response.headers.get("Content-Type"),
    )
    return flask_response


@siyavula_bp.post(
    "/activity/answer", tags=[siyavula_tag], responses={200: SiyavulaModel}
)
@basic_auth.login_required
@depends_on_siyavula_api
def practice_submit_answer(body: SiyavulaCreateAnswersModel):
    """
    Submit a student's answers for marking
    """

    api = SiyavulaUserAPI(client_token=g.siavula_api.client_token, user_id=body.user_id)
    siyavula_response = api.practice_submit_answer(
        activity_uuid=body.activity_uuid,
        response_uuid=body.response_uuid,
        form_data=body.answers,
    )

    flask_response = Response(
        siyavula_response.content,
        status=siyavula_response.status_code,
        content_type=siyavula_response.headers.get("Content-Type"),
    )
    return flask_response


@siyavula_bp.post("/activity/next", tags=[siyavula_tag], responses={200: SiyavulaModel})
@basic_auth.login_required
@depends_on_siyavula_api
def practice_next(body: SiyavulaCreateModel):
    """
    Next question
    """

    api = SiyavulaUserAPI(client_token=g.siavula_api.client_token, user_id=body.user_id)
    siyavula_response = api.practice_next_question(
        activity_uuid=body.activity_uuid, response_uuid=body.response_uuid
    )

    flask_response = Response(
        siyavula_response.content,
        status=siyavula_response.status_code,
        content_type=siyavula_response.headers.get("Content-Type"),
    )
    return flask_response


@siyavula_bp.post(
    "/activity/retry", tags=[siyavula_tag], responses={200: SiyavulaModel}
)
@basic_auth.login_required
@depends_on_siyavula_api
def practice_retry(body: SiyavulaCreateModel):
    """
    Retry the activity.
    """

    api = SiyavulaUserAPI(client_token=g.siavula_api.client_token, user_id=body.user_id)
    siyavula_response = api.practice_retry(
        activity_uuid=body.activity_uuid, response_uuid=body.response_uuid
    )

    flask_response = Response(
        siyavula_response.content,
        status=siyavula_response.status_code,
        content_type=siyavula_response.headers.get("Content-Type"),
    )
    return flask_response
