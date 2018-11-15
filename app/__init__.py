from flask import Flask
import logging
import os

from . import db
from app import users


def create_app(config_name='default'):
    app = Flask(__name__, instance_relative_config=True)

    configs = {
        "development": "app.config.DevelopmentConfig",
        "testing": "app.config.TestingConfig",
        "default": "app.config.DevelopmentConfig",
        "production": "app.config.BaseConfig"
    }


    app.config.from_object(configs[config_name])
    app.register_blueprint(users.bp)

    db.init_app(app)
    file_handler = logging.FileHandler('./logs/app.log')
    app.logger.addHandler(file_handler)
    return app

app = create_app()
if __name__ == "__main__":
    app.run(os.getenv("FLASK_ENV"))
