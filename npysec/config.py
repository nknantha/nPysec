import os
from datetime import timedelta

# For debugging purpose.
DEBUG = False

# General Configurations.
FLASK_TITLE = "nPysec"
SECRET_KEY = os.environ["FLASK_SECRET"]
PROJECT_URL = "https://github.com/nknantha/nPysec"

# Flask-Seasurf Configurations.
CSRF_COOKIE_NAME = "ss_csrf_token"
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_TIMEOUT = timedelta(days=1)
CSRF_COOKIE_HTTPONLY = True

# Flask-Login Configurations.
REMEMBER_COOKIE_SECURE = True
REMEMBER_COOKIE_TIMEOUT = timedelta(days=1)
REMEMBER_COOKIE_HTTPONLY = True
login_manager_login_view = "main.signin"
login_manager_login_message_category = "error"
login_manager_session_protection = "strong"

# Flask-SQLAlchemy Configurations.
def get_db_uri(uri: str) -> str:
    """
    To maintain SQLAlchemy compatibility with Heroku, this function 
    changes the Database URI from `postgres://` to `postgresql://`.
    """
    if uri.startswith("postgres://"):
        return uri.replace("postgres://", "postgresql://", 1)
    return uri

SQLALCHEMY_DATABASE_URI = get_db_uri(os.environ["DATABASE_URL"])
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-Talisman Configurations.
csp_self = "'self'"
custom_csp_policy = {
    "default-src": csp_self,
    "img-src": [
        csp_self,
        "data:"
    ],
    "style-src": [
        csp_self,
        "fonts.googleapis.com",
        "cdn.jsdelivr.net"
    ],
    "font-src": [
        csp_self,
        "fonts.gstatic.com"
    ],
    "script-src": [
        csp_self,
        "cdn.jsdelivr.net"
    ]
}

img_view_csp = {
    "default-src": csp_self,
    "style-src": [
        csp_self,
        "'unsafe-inline'"
    ]
}
