from flask import Flask
import logging
import os

from app.registry import RegistryResource
from . import db
from . import get_stripe
from app import auth


def create_app(config_name='default'):
    app = Flask(__name__, instance_relative_config=True)

    configs = {
        "development": "app.config.DevelopmentConfig",
        "testing": "app.config.TestingConfig",
        "default": "app.config.DevelopmentConfig",
        "production": "app.config.BaseConfig"
    }

    app.config.from_object(configs[config_name])

    get_stripe.init_app(app)
    db.init_app(app)
    file_handler = logging.FileHandler('./logs/app.log')
    app.logger.addHandler(file_handler)

    registry_resource = RegistryResource()

    app.register_blueprint(auth.bp)
    app.register_blueprint(registry_resource.bp)

    return app

app = create_app()
if __name__ == "__main__":
    app.run(os.getenv("FLASK_ENV"))
