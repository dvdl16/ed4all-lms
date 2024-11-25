from typing import Dict
import httpx

from lms_backend.app.config import Config
from lms_backend.app.models import User
from lms_backend.app.db import db
from lms_backend.app.utils import is_valid_uuid
from flask import g
import logging
import secrets
from functools import wraps


def depends_on_siyavula_api(f):
    """
    Decorator that checks if the Siyavula API client is available in g
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        if not hasattr(g, "siavula_api") or not g.siavula_api:
            instantiate_siyavula()
        return f(*args, **kwargs)

    return wrapper


class SiyavulaAPI:
    """
    Class for managing Siyavula API
    """

    def __init__(self, name: str, password: str, region: str, curriculum: str) -> None:
        """
        Initialise the API
            name: the organisation name provided by Siyavula
            password: the password that was provided by Siyavula
            region: The country the template will be requested for
            curriculum: The curriculum the template will be requested for
        """
        self.name = name
        self.password = password
        self.region = region
        self.curriculum = curriculum
        self.client_token = None

        self.get_client_token()

    def get_client_token(self):
        """
        Retrieves an authentication token to be used to authenticate us in subsequent requests
        """
        url = "https://www.siyavula.com/api/siyavula/v1/get-token"
        payload = {
            "name": self.name,
            "password": self.password,
            "region": self.region,
            "curriculum": self.curriculum,
        }
        response = httpx.post(url, json=payload)
        self.client_token = response.json()["token"]


class SiyavulaUserAPI:
    def __init__(self, client_token: str, user_id: int) -> None:
        self.client_token = client_token
        self.user = User.query.filter_by(id=user_id).first()
        if not self.user:
            raise ValueError("Unexpected User ID")
        self.user_token = None

    def get_or_create_user_token(self):
        """
        Gets a user token if user exists on Siavula, else create user and get token
        """
        if not self.user.siyavula_account_id:
            self.create_siavula_user_id()

        self.get_user_token()

    def get_user_token(self):
        """
        Retrieves an authentication token to authenticate a user
        """
        url = f"https://www.siyavula.com/api/siyavula/v1/user/{self.user.id}/token"
        headers = {"JWT": self.client_token}
        response = httpx.get(url, headers=headers)
        self.user_token = response.json()["token"]

    def create_siavula_user_id(self):
        """
        Create user on Siavula
        """
        url = "https://www.siyavula.com/api/siyavula/v1/user"
        headers = {"JWT": self.client_token}
        payload = {
            "external_user_id": str(self.user.id),
            "password": secrets.token_urlsafe(10),
            "role": self.user.role,
            "name": self.user.name,
            "surname": self.user.surname,
            "grade": int(self.user.grade),
            "country": self.user.country,
            "curriculum": self.user.curriculum,
            "email": self.user.email,
        }

        response = httpx.post(url, headers=headers, json=payload)
        self.user.siyavula_account_id = response.json()["uuid"]
        db.session.commit()

    def create_practice_activity(self, section_id: int) -> httpx.Response:
        """
        Create a practice activity
            section_id: The section ID to be practised. Can be retrieved from the ToC endpoint.
        """
        self.get_or_create_user_token()

        if type(section_id) is not int:
            raise ValueError("Unexpected section ID")

        url = f"https://www.siyavula.com/api/siyavula/v1/activity/create/practice/{section_id}"
        headers = {"JWT": self.client_token, "Authorization": f"JWT {self.user_token}"}

        response = httpx.get(url, headers=headers)
        return response

    def practice_submit_answer(
        self, activity_uuid: str, response_uuid: str, form_data: Dict
    ) -> httpx.Response:
        """
        Submit a student's answers for marking
            activity_uuid: The activity uuid returned in the create activity response.
            response_uuid: The response uuid returned in the create activity response.
        """
        self.get_or_create_user_token()

        if not is_valid_uuid(activity_uuid) or not is_valid_uuid(response_uuid):
            raise ValueError("Unexpected uuids")

        url = f"https://www.siyavula.com/api/siyavula/v1/activity/{activity_uuid}/response/{response_uuid}/submit-answer"
        headers = {"JWT": self.client_token, "Authorization": f"JWT {self.user_token}"}

        response = httpx.post(url, headers=headers, data=form_data)
        return response

    def practice_next_question(
        self, activity_uuid: str, response_uuid: str
    ) -> httpx.Response:
        """
        Practice next question
            activity_uuid: The activity uuid returned in the create activity response.
            response_uuid: The response uuid returned in the create activity response.
        """
        self.get_or_create_user_token()

        if not is_valid_uuid(activity_uuid) or not is_valid_uuid(response_uuid):
            raise ValueError("Unexpected uuids")

        url = f"https://www.siyavula.com/api/siyavula/v1/activity/{activity_uuid}/response/{response_uuid}/next"
        headers = {"JWT": self.client_token, "Authorization": f"JWT {self.user_token}"}

        response = httpx.get(url, headers=headers)
        return response

    def practice_retry(self, activity_uuid: str, response_uuid: str) -> httpx.Response:
        """
        Practice retry
            activity_uuid: The activity uuid returned in the create activity response.
            response_uuid: The response uuid returned in the create activity response.
        """
        self.get_or_create_user_token()

        if not is_valid_uuid(activity_uuid) or not is_valid_uuid(response_uuid):
            raise ValueError("Unexpected uuids")

        url = f"https://www.siyavula.com/api/siyavula/v1/activity/{activity_uuid}/response/{response_uuid}/retry"
        headers = {"JWT": self.client_token, "Authorization": f"JWT {self.user_token}"}

        response = httpx.get(url, headers=headers)
        return response


def instantiate_siyavula():
    try:
        g.siavula_api = SiyavulaAPI(
            name=Config.SIAVULA_API_CLIENT_NAME,
            password=Config.SIAVULA_API_CLIENT_PASS,
            region=Config.SIAVULA_API_CLIENT_REGION,
            curriculum=Config.SIAVULA_API_CLIENT_CURRICULUM,
        )

    except Exception:
        logging.critical("Failed to connect to Siyavula API", exc_info=True)
