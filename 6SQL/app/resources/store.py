from uuid import uuid4
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.db import stores
from app.schemas import StoreSchema

blp = Blueprint("Stores", __name__, description="Operations on stores")


@blp.route("/store")
class Store(MethodView):
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, req):
        for store in stores.values():
            if store["name"] == req["name"]:
                return abort(400, message="Bad Request. The store already exists")
        store_id = uuid4().hex
        new_store = req | {"id": store_id}
        stores[store_id] = new_store
        return new_store, 201

    @blp.response(200, StoreSchema(many=True))
    def get(self):  # http://127.0.0.1:5000/store
        return stores.values()


@blp.route("/store/<string:store_id>")
class StoreID(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message=f"Store not found")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted"}
        except KeyError:
            abort(404, message=f"Store not found")
