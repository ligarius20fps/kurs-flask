from uuid import uuid4
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.db import items, stores
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item")
class Item(MethodView):
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, req):
        store_id = req["store_id"]
        for item in items.values():
            if (item["name"] == req["name"] and
                    item["store_id"] == req["store_id"]):
                return abort(400, message="Bad Request. The item already exists")
        if store_id not in stores:
            abort(404, message=f"Store not found")
        item_id = uuid4().hex
        new_item = req | {"id": item_id}
        items[item_id] = new_item
        return new_item, 201

    @blp.response(200, ItemSchema(many=True))
    def get(self):  # http://127.0.0.1:5000/item
        return items.values()


@blp.route("/item/<string:item_id>")
class ItemID(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message=f"Item not found")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, req, item_id):
        if item_id not in items.keys():
            abort(404, message=f"Item not found")
        for field in {"name", "price"}:
            if field in req.keys():
                items[item_id][field] = req[field]
        return items[item_id]

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted"}
        except KeyError:
            abort(404, message=f"Item not found")
