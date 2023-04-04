from uuid import uuid4

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores

blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item")
class Item(MethodView):
    def post(self):
        req = request.get_json()
        # name – string
        # price – float.2
        # store_id – uuid
        if {"name", "price", "store_id"} != req.keys():
            return abort(400, message="Bad Request. "
                                      "Only 'name', 'price' and 'store_id' should be included in the JSON payload.")
        store_id = req["store_id"]
        for item in items.values():
            if (item["name"] == req["name"] and
                    item["store_id"] == req["store_id"]):
                return abort(400, message="Bad Request. The item already exists.")
        if store_id not in stores:
            abort(404, message=f"Store with ID {store_id} not found")
        item_id = uuid4().hex
        new_item = req | {"item_id": item_id}
        items[item_id] = new_item
        return new_item, 201

    def get(self):  # http://127.0.0.1:5000/item
        return {"items": list(items.values())}


@blp.route("/item/<string:item_id>")
class ItemID(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message=f"Item not found")

    def put(self, item_id):
        req = request.get_json()
        fields = {"name", "price"}
        if fields & req.keys() == set():
            return abort(400, message="Bad Request. 'name' or 'price' should be included in the JSON payload.")
        if item_id not in items.keys():
            abort(404, message=f"Item not found")
        for field in fields:
            if field in req.keys():
                items[item_id][field] = req[field]
        return items[item_id]

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted"}
        except KeyError:
            abort(404, message=f"Item not found")
