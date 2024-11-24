from flask_httpauth import HTTPBasicAuth
from lms_backend.app.models import User
from werkzeug.security import check_password_hash

basic_auth = HTTPBasicAuth()


@basic_auth.verify_password
def verify_password(username, password):
    """
    Get the user from the database and verify password
    """
    user = User.query.filter_by(email=username).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None
