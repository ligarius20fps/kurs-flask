import os

import requests
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, get_jwt_identity
from blocklist import BLOCKLIST
from models import UserModel
from schemas import UserSchema, UserRegisterSchema

blp = Blueprint("Users", __name__, description="Operations on users")

def send_simple_message(to, subject, body):
    domain = os.getenv("MAILGUN_DOMAIN")
    return requests.post(
		f"https://api.mailgun.net/v3/{domain}/messages",
		auth=("api", os.getenv("MAILGUN_API_KEY")),
		data={"from": f"mati <mailgun@{domain}>",
			"to": [to],
			"subject": subject,
			"text": body})

@blp.route("/register")
class RegisterUser(MethodView):
    @blp.arguments(UserRegisterSchema)
    @blp.response(200)
    def post(self, req):
        new_user = UserModel(**req)
        new_user.password = pbkdf2_sha256.hash(req["password"])
        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            abort(409, message="User with such username or email already exists")
        except SQLAlchemyError as e:
            abort(500, message=e)
        send_simple_message(
            to=new_user.email,
            subject="Successfully signed up",
            body=f"Hello, {new_user.username} and welcome to stores REST API"
        )
        return {"message": "Successfully created a user"}

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(200)
    def post(self, req):
        user = UserModel.query.filter(
            UserModel.username == req["username"]
        ).first()
        if user and pbkdf2_sha256.verify(req["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}
        abort(401, message="Invalid credentials")


@blp.route("/user/<int:user_id>")
class UserID(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, user_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required")
        return UserModel.query.get_or_404(user_id)

    @jwt_required(fresh=True)
    @blp.response(200)
    def delete(self, user_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required")
        user = UserModel.query.get_or_404(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=e)
        return {"message": "User successfully deleted"}

@blp.route("/logout")
class LogoutUser(MethodView):
    @jwt_required()
    @blp.response(200)
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}

@blp.route("/refresh")
class RefreshToken(MethodView):
    @jwt_required(refresh=True)
    @blp.response(200)
    def post(self):
        identity = get_jwt_identity()
        nonfresh_access_token = create_access_token(identity=identity, fresh=False)
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": nonfresh_access_token}
