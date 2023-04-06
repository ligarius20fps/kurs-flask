from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item")
class Item(MethodView):
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, req):
        new_item = ItemModel(**req)
        try:
            db.session.add(new_item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured")
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
