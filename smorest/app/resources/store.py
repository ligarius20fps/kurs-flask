from uuid import uuid4
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

blp = Blueprint("Stores", __name__, description="Operations on stores")


@blp.route("/store")
class Store(MethodView):
    def post(self):
        req = request.get_json()
        # name – string
        if {"name"} != req.keys():
            return abort(400, message="Bad Request. Only 'name' should be included in the JSON payload.")
        for store in stores.values():
            if store["name"] == req["name"]:
                return abort(400, message="Bad Request. The store already exists.")
        store_id = uuid4().hex
        new_store = req | {"store_id": store_id}
        stores[store_id] = new_store
        return new_store, 201

    def get(self):  # http://127.0.0.1:5000/store
        return {"stores": list(stores.values())}


@blp.route("/store/<string:store_id>")
class StoreID(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message=f"Store not found")

    def delete(self, store_id):
        # shouldn't we also delete items in the deleted store?
        try:
            del stores[store_id]
            return {"message": "Store deleted"}
        except KeyError:
            abort(404, message=f"Store not found")
