from os import getenv
from flask_jwt_extended import JWTManager
from flask import Flask, jsonify
from flask_smorest import Api
from db import db
from resources.store import blp as StoreBlueprint
from resources.item import blp as ItemBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint
from blocklist import BLOCKLIST

def create_app(db_url=None):
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"  # http://127.0.0.1:5000/docs
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["JWT_SECRET_KEY"] = "słabe_hasło"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 10 * 60 # https://flask-jwt-extended.readthedocs.io/en/stable/options/#JWT_ACCESS_TOKEN_EXPIRES

    db.init_app(app)
    api = Api(app)

    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims(identity):
        return {"is_admin": identity == 1}

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(header, payload):
        return payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def token_revoked(header, payload):
        return jsonify({
            "message": "The token has been revoked",
            "error": "token_revoked"
        }), 401

    @jwt.expired_token_loader
    def token_expired(header, payload):
        return jsonify({
            "message": "The token has expired",
            "error": "token_expired"
        }), 401

    @jwt.invalid_token_loader
    def invalid_token(reason):
        return jsonify({
            "message": "The token is invalid",
            "error": "invalid_token",
            "reason": reason
        }), 400

    @jwt.unauthorized_loader
    def unauthorirzed(reason):
        return jsonify({
            "message": "Request does not contain an access token",
            "error": "unauthorised",
            "reason": reason
        }), 401

    with app.app_context():
        db.create_all()

    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
