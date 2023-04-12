from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt
from blocklist import BLOCKLIST
from models import UserModel
from schemas import UserSchema

blp = Blueprint("Users", __name__, description="Operations on users")

@blp.route("/register")
class RegisterUser(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(200)
    def post(self, req):
        new_user = UserModel(**req)
        new_user.password = pbkdf2_sha256.hash(req["password"])
        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            abort(409, message="User with such username already exists")
        except SQLAlchemyError as e:
            abort(500, message=e)
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
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}
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

    @jwt_required()
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
    @jwt_required()
    @blp.response(200)
    def post(self):
        pass
