from flask import Flask

from . import routes

app = Flask(__name__, template_folder="templates")
routes.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)  # noqa: S201
