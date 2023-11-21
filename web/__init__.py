from flask import Flask
from datetime import timedelta, datetime
from controller import Control


def create_app(config_file="config.py"):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    app.permanent_session_lifetime = timedelta(minutes=1)
    app.register_blueprint(Control)
    return app
