from base64 import b64encode
import unittest
from lms_backend.app.config import TestingConfig
from lms_backend.app.models import User
from lms_backend.app import create_app, db
from werkzeug.security import generate_password_hash


class TestAuthBlueprint(unittest.TestCase):
    def setUp(self):
        """
        Set up a test client and in-memory database
        """
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app.app_context().push()

        self.add_test_user()

        self.basic_auth_header = convert_to_basic_auth(
            TestingConfig.DEMO_USER_NAME, TestingConfig.DEMO_USER_PASS
        )

    def tearDown(self):
        """
        Clean up the database
        """
        db.session.remove()
        db.drop_all()

    def add_test_user(self):
        """
        Add a test user to the database
        """
        test_user = User(
            email="existing@example.com",
            name="Existing",
            surname="User",
            password_hash=generate_password_hash("password123"),
            grade="10",
            country="ZA",
            curriculum="CAPS",
            role="Learner",
        )
        db.session.add(test_user)
        db.session.commit()

    def test_create_user_success(self):
        """
        Test creating a user successfully
        """
        user_data = {
            "email": "newuser@example.com",
            "name": "New",
            "surname": "User",
            "password": "SecurePass123!",
            "grade": "10",
            "country": "ZA",
            "curriculum": "CAPS",
            "role": "Learner",
        }

        response = self.client.post(
            "/auth/users",
            json=user_data,
            headers={
                "Authorization": self.basic_auth_header,  # Mock Basic Auth Header
            },
        )

        # Assertions
        self.assertEqual(response.status_code, 201)
        created_user = response.get_json()
        self.assertEqual(created_user["email"], user_data["email"])
        self.assertEqual(created_user["name"], user_data["name"])

        # Verify user was added to the database
        user_in_db = User.query.filter_by(email="newuser@example.com").first()
        self.assertIsNotNone(user_in_db)
        self.assertEqual(user_in_db.name, "New")

    def test_create_user_conflict(self):
        """
        Test creating a user when the email already exists
        """
        user_data = {
            "email": "existing@example.com",
            "name": "Test",
            "surname": "User",
            "password": "SecurePass123!",
            "grade": "10",
            "country": "ZA",
            "curriculum": "CAPS",
            "role": "Learner",
        }

        response = self.client.post(
            "/auth/users",
            json=user_data,
            headers={
                "Authorization": self.basic_auth_header,
            },
        )

        # Assertions
        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response.get_json(), {"message": "User with this email already exists"}
        )

    def test_get_users(self):
        """
        Test retrieving all users
        """
        response = self.client.get(
            "/auth/users",
            headers={
                "Authorization": self.basic_auth_header,
            },
        )

        # Assertions
        self.assertEqual(response.status_code, 200)
        users = response.get_json()

        # Verify the test user, and the demo user is returned
        self.assertEqual(len(users), 2)
        self.assertEqual(users[1]["email"], "existing@example.com")
        self.assertEqual(users[1]["name"], "Existing")


def convert_to_basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
    return f"Basic {token}"
