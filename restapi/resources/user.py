# resources/tag.py

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token,create_refresh_token, get_jwt_identity, jwt_required, get_jwt
from sqlalchemy import or_

from restapi.models import UserModel
from restapi.schemas.schemas import UserSchema, UserRegisterSchema
from restapi.db import db

from restapi.blocklists.blocklist import BLOCKLIST

import requests
from dotenv import load_dotenv
import os

load_dotenv()

blp = Blueprint("Users", "users", __name__, description="Operations on Users")

def send_simple_message(to, subject, body):
    domain = os.getenv("MAILGUN_DOMAIN")
    api_key = os.getenv("MAILGUN_API_KEY")
    return requests.post(
		f"https://api.mailgun.net/v3/{domain}/messages",
		auth=("api", {api_key}),
		data={"from": f"RamaManohar <mailgun@{domain}>",
			"to": [to],
			"subject": subject,
			"text": body})


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        if UserModel.query.filter(
            or_(UserModel.username == user_data["username"],
                UserModel.email == user_data["email"]
                )).first():
            abort(409,
                  message="username already exists")
        
        user = UserModel(
            username = user_data["username"],
            email = user_data["email"],
            password = pbkdf2_sha256.hash(user_data["password"])
        )

        db.session.add(user)
        db.session.commit()

        send_simple_message(
            to = user.email,
            subject ="successfully registered",
            body = f"Hi {user.username}, you have successfully signed up to the stores REST API"
        )

        return {"message" : "user created"}

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
       user = UserModel.query.get_or_404(user_id)
       return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "user deleted"}, 200
    


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token" : refresh_token}

        abort(401,
              message="Invalid Credentials")


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message" : "successfully logged out"}

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token" : new_token}