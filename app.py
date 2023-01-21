import os
from flask import Flask

from flask_smorest import Api
from flask_jwt_extended import JWTManager

from db import db

from resources.record import blp as RecordBlueprint
from resources.user import blp as UserBlueprint

from flask_cors import *

app = Flask(__name__)

CORS(app, resources=r'/*')

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

api = Api(app)

app.config["JWT_SECRET_KEY"] = "Jason"
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

api.register_blueprint(RecordBlueprint)
api.register_blueprint(UserBlueprint)
