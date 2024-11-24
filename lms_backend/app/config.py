import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///lms.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEMO_USER_NAME = os.environ.get("DEMO_USER_NAME", "foo@bar.co")
    DEMO_USER_PASS = os.environ.get("DEMO_USER_PASS", "changeme")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    DEBUG = False
    DEMO_USER_NAME = "test@user.com"
    DEMO_USER_PASS = "test_pass"
