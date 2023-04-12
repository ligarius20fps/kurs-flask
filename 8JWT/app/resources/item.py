from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item")
class Item(MethodView):
    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema, description="Adds an item")
    @blp.alt_response(500, description="Returned if there is an error in the database")
    def post(self, req):
        new_item = ItemModel(**req)
        try:
            db.session.add(new_item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return new_item, 201

    @blp.response(200, ItemSchema(many=True), description="Returns all items in the database")
    def get(self):  # http://127.0.0.1:5000/item
        return ItemModel.query.all()


@blp.route("/item/<int:item_id>")
class ItemID(MethodView):
    @blp.response(200, ItemSchema, description="Returns an item with provided ID")
    @blp.alt_response(404, description="Returned if no item found with such ID",
                      example={
                        "code": 404,
                        "status": "Not Found"
                    })
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema, description="Creates or updates an item in the database")
    @blp.alt_response(500, description="Returned if there is an error in the database")
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
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return item

    @jwt_required(fresh=True)
    @blp.response(200, description="Deletes an item with provided ID", example={"message": "Item successfully deleted"})
    @blp.alt_response(404, description="Returned if no item found with such ID",
                      example={
                        "code": 404,
                        "status": "Not Found"
                    })
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item successfully deleted"}
