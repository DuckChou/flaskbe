from flask import request
from flask.views import MethodView

from flask_smorest import Blueprint, abort

from schemas import UserSchemaForSignup, UserSchemaForLogin

from db import UserModel, db

from sqlalchemy.exc import SQLAlchemyError

from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token

blp = Blueprint("users", __name__, description="Operations on users")




@blp.route("/login")
class Login(MethodView):

    @blp.arguments(UserSchemaForLogin)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.user_id)
            return {"access_token": access_token, "user_id": user.user_id, "first_name": user.firstname}

        abort(401, message="Invalid credentials")


@blp.route("/signup")
class Signup(MethodView):

    @blp.arguments(UserSchemaForSignup)
    def post(self, user_data):
        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
            firstname=user_data["firstname"]
        )

        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="A user with that username already exists")

        db.session.add(user)
        db.session.flush()
        user_id = user.user_id
        firstname = user.firstname
        db.session.commit()

        access_token = create_access_token(identity=user.user_id)

        return {"mes": "user created","user_id":user_id,"firstname":firstname,"access_token":access_token}, 201

