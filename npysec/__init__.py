from flask import Flask
from flask_login import LoginManager
from flask_minify import Minify
from flask_seasurf import SeaSurf
from flask_talisman import Talisman

from . import config
from .forms import wtf_is_hidden_field
from .models import db, User

talis = Talisman()
logman = LoginManager()
seasurf = SeaSurf()
minify = Minify()


def create_app(app=None):
    if not app:
        app = Flask(__name__)
    app.config.from_object(config)
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.strip_trailing_newlines = False
    app.jinja_env.globals['wtf_is_hidden_field'] = wtf_is_hidden_field

    # Data Base Initialization.
    db.init_app(app=app)

    # SeaSurf Initialization.
    seasurf.init_app(app=app)

    # Talisman Initialization.
    talis.init_app(app=app, content_security_policy=config.custom_csp_policy)

    # Minify Initialization.
    minify.init_app(app=app)

    # Login Manager Initialization.
    logman.init_app(app=app)
    logman.login_view = config.login_manager_login_view
    logman.login_message_category = config.login_manager_login_message_category
    logman.session_protection = config.login_manager_session_protection
    logman.user_loader(lambda user_id: User.query.get(user_id))

    # Registering main blueprints.
    from .views import main
    app.register_blueprint(main)

    return app

# Creating db tables on initialization of package.
db.create_all(app=create_app())