import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///lms.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEMO_USER_NAME = os.environ.get("DEMO_USER_NAME", "foo@bar.co")
    DEMO_USER_PASS = os.environ.get("DEMO_USER_PASS", "changeme")

    SIAVULA_API_CLIENT_NAME = os.environ.get("SIAVULA_API_CLIENT_NAME")
    SIAVULA_API_CLIENT_PASS = os.environ.get("SIAVULA_API_CLIENT_PASS")
    SIAVULA_API_CLIENT_REGION = os.environ.get("SIAVULA_API_CLIENT_REGION", "ZA")
    SIAVULA_API_CLIENT_CURRICULUM = os.environ.get(
        "SIAVULA_API_CLIENT_CURRICULUM", "CAPS"
    )


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    DEBUG = False
    DEMO_USER_NAME = "test@user.com"
    DEMO_USER_PASS = "test_pass"
