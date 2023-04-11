from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from passlib.hash import pbkdf2_sha256

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

@blp.route("/user/<int:user_id>")
class UserID(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        return UserModel.query.get_or_404(user_id)

    @blp.response(200)
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=e)
        return {"message": "User successfully deleted"}
