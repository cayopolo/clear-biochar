import os

from flask import Flask

from . import routes

app = Flask(__name__, template_folder="templates")

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-change-in-production")

routes.init_app(app)
