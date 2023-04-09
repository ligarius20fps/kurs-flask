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
        return ItemModel.query.all()


@blp.route("/item/<string:item_id>")
class ItemID(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, req, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = req["price"]
            item.name = req["name"]
        else:
            item = ItemModel(id=item_id, **req)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured")
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item successfully deleted"}
