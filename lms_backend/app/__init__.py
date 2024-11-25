from typing import Optional
from lms_backend.app.db import db
from lms_backend.app.users.routes import auth_bp
from lms_backend.app.courses.routes import courses_bp
from lms_backend.app.siyavula.routes import siyavula_bp
from lms_backend.app.config import Config

from flask_openapi3 import OpenAPI, Info

from lms_backend.app.utils import create_demo_user, create_standard_courses

# OpenAPI Spec details
info = Info(title="LMS API", version="0.1.0")
basic_auth = {"type": "http", "scheme": "basic"}
security_schemes = {"basic": basic_auth}
security = [{"jwt": []}]


def create_app(config: Optional[Config] = None):
    """
    Main function to initialise Flask app and register blueprints
    """
    app = OpenAPI(__name__, info=info, security_schemes=security_schemes)
    if not config:
        config = Config
    app.config.from_object(config)

    # Initialize
    db.init_app(app)
    with app.app_context():
        db.create_all()
        # Demo data
        create_demo_user(config)
        create_standard_courses()

    # Register blueprints
    app.register_api(auth_bp)
    app.register_api(courses_bp)
    app.register_api(siyavula_bp)

    return app
