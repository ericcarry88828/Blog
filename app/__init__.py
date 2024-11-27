import os
from flask import Flask
from flask_wtf import CSRFProtect
from flask_bootstrap import Bootstrap5


def create_app():
    app = Flask(__name__)
    app.secret_key = "secret_key"
    CSRFProtect(app)
    Bootstrap5(app)

    app.config['BASE_DIR'] = os.path.dirname(os.path.abspath(__file__))
    app.config['WTF_CSRF_CHECK_DEFAULT'] = False

    from . import blog, auth, admin
    app.register_blueprint(blog.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    return app
