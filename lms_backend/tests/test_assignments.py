import unittest
from base64 import b64encode
from lms_backend.app.config import TestingConfig
from lms_backend.app.models import User, Course, UserCourse
from lms_backend.app import create_app, db


class TestAssignmentsBlueprint(unittest.TestCase):
    def setUp(self):
        """
        Set up a test client and in-memory database
        """
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app.app_context().push()

        self.add_test_data()

        self.basic_auth_header = convert_to_basic_auth(
            TestingConfig.DEMO_USER_NAME, TestingConfig.DEMO_USER_PASS
        )

    def tearDown(self):
        """
        Clean up the database
        """
        db.session.remove()
        db.drop_all()

    def add_test_data(self):
        """
        Add test users and courses to the database
        """
        test_user = User(
            email="existing_user@example.com",
            name="Existing",
            surname="User",
            password_hash="wololo",
            grade="10",
            country="ZA",
            curriculum="CAPS",
            role="Learner",
        )
        db.session.add(test_user)

        test_course = Course(name="Test Course")
        db.session.add(test_course)

        db.session.commit()

    def test_assign_course_success(self):
        """
        Test assigning a course to a user successfully
        """
        assignment_data = {
            "user_id": 1,
            "course_id": 1,
        }

        response = self.client.post(
            "/assignments",
            json=assignment_data,
            headers={"Authorization": self.basic_auth_header},
        )

        # Assertions
        self.assertEqual(response.status_code, 201)
        assignment = response.get_json()
        self.assertEqual(assignment["user_id"], assignment_data["user_id"])
        self.assertEqual(assignment["course_id"], assignment_data["course_id"])

        # Verify the assignment was added to the database
        user_course = UserCourse.query.filter_by(user_id=1, course_id=1).first()
        self.assertIsNotNone(user_course)

    def test_assign_course_conflict(self):
        """
        Test assigning a course that is already assigned
        """
        # Add an existing assignment
        user_course = UserCourse(user_id=1, course_id=1)
        db.session.add(user_course)
        db.session.commit()

        assignment_data = {
            "user_id": 1,
            "course_id": 1,
        }

        response = self.client.post(
            "/assignments",
            json=assignment_data,
            headers={"Authorization": self.basic_auth_header},
        )

        # Assertions
        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response.get_json(), {"message": "User-Course Assignment already exists"}
        )

    def test_assign_course_user_not_found(self):
        """
        Test assigning a course to a non-existent user
        """
        assignment_data = {
            "user_id": 999,
            "course_id": 1,
        }

        response = self.client.post(
            "/assignments",
            json=assignment_data,
            headers={"Authorization": self.basic_auth_header},
        )

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(), {"message": "User with this id does not exist"}
        )

    def test_assign_course_not_found(self):
        """
        Test assigning a non-existent course to a user
        """
        assignment_data = {
            "user_id": 1,
            "course_id": 999,
        }

        response = self.client.post(
            "/assignments",
            json=assignment_data,
            headers={"Authorization": self.basic_auth_header},
        )

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(), {"message": "Course with this id does not exist"}
        )


def convert_to_basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
    return f"Basic {token}"
