import uuid
from logging.config import dictConfig

from flask import Flask
from flask_cors import CORS

from example_backend.comments import controller as comments_controller
from example_backend.exc.bad_request import BadRequest, handle_bad_request
from example_backend.exc.not_found import NotFound, handle_not_found
from example_backend.extensions import alchemydumps, db, migrate
from example_backend.posts import controller as posts_controller
from example_backend.users import controller as users_controller

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            },
            "out": {
                "class": "logging.FileHandler",
                "filename": "/tmp/example.log",
                "formatter": "default",
            },
        },
        "root": {"level": "INFO", "handlers": ["out", "wsgi"]},
    }
)


def create_app(config_object="example_backend.settings"):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.config["SECRET_KEY"] = str(uuid.uuid4())

    CORS(app)

    app.register_error_handler(BadRequest, handle_bad_request)
    app.register_error_handler(NotFound, handle_not_found)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    alchemydumps.init_app(app, db)


def register_blueprints(app):
    app.register_blueprint(users_controller.blueprint)
    app.register_blueprint(posts_controller.blueprint)
    app.register_blueprint(comments_controller.blueprint)
