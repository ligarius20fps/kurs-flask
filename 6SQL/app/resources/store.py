from uuid import uuid4
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from schemas import StoreSchema
from models import StoreModel

blp = Blueprint("Stores", __name__, description="Operations on stores")


@blp.route("/store")
class Store(MethodView):
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, req):
        new_store = StoreModel(**req)
        try:
            db.session.add(new_store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="The store already exists")
        except SQLAlchemyError:
            abort(500, message="An error occured")
        return new_store, 201

    @blp.response(200, StoreSchema(many=True))
    def get(self):  # http://127.0.0.1:5000/store
        return StoreModel.query.all()


@blp.route("/store/<string:store_id>")
class StoreID(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        try:
            db.session.delete(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured")
        return {"message": "Store successfully deleted"}
