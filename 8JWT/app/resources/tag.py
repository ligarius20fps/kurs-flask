from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, ItemAndTagSchema

blp = Blueprint("Tags", __name__, description="Operations on tags")


@blp.route("/store/<int:store_id>/tag")
class TagStoreID(MethodView):
    @jwt_required()
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema, description="Adds a tag to the store with provided ID")
    @blp.alt_response(500, description="Returned if there is an error in the database")
    def post(self, req, store_id):
        new_tag = TagModel(**req, store_id=store_id)
        try:
            db.session.add(new_tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return new_tag, 201

    @blp.response(200, TagSchema(many=True), description="Returns all tags associated with the store provided in ID")
    @blp.alt_response(404, description="Returned id no store found with such ID",
                      example={
                        "code": 404,
                        "status": "Not Found"
                    })
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()


@blp.route("/tag/<int:tag_id>")
class TagID(MethodView):
    @blp.response(200, TagSchema, description="Returns a tag with provided ID")
    @blp.alt_response(404, description="Returned if no tag found with such ID",
                      example={
                        "code": 404,
                        "status": "Not Found"
                    })
    def get(self, tag_id):
        return TagModel.query.get_or_404(tag_id)

    @jwt_required(fresh=True)
    @blp.response(200, description="Deletes a tag with no items associated with it",
                  example={"message": "Tag successfully deleted"})
    @blp.alt_response(400, description="Returned if attempted to delete a tag that has items associated with it",
                      example={
                        "code": 400,
                        "message": "Can't delete a tag with items associated with it",
                        "status": "Bad Request"
                    })
    @blp.alt_response(500, description="Returned if there is an error in the database")
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        if not tag.items:
            try:
                db.session.delete(tag)
                db.session.commit()
            except Exception as e:
                abort(500, message=str(e))
        else:
            abort(400, message="Can't delete a tag with items associated with it")
        return {"message": "Tag successfully deleted"}


@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class ItemIDTagId(MethodView):
    @jwt_required()
    @blp.response(200, TagSchema, description="Links item with tag, both identified by ID")
    @blp.alt_response(400, description="Returned if item and tag do not belong to the same store",
                      example={
                        "code": 400,
                        "message": "Item and Tag must belong to the same store",
                        "status": "Bad Request"
                    })
    @blp.alt_response(404, description="Returned if either item or tag were not found",
                      example={
                        "code": 404,
                        "status": "Not Found"
                    })
    @blp.alt_response(500, description="Returned if there is an error in the database")
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        if item.store.id != tag.store.id:
            abort(400, message="Item and Tag must belong to the same store")
        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return tag

    @jwt_required(fresh=True)
    @blp.response(200, ItemAndTagSchema, description="Unlinks tag from the item, both identified by ID")
    @blp.alt_response(400, description="Returned if item and tag are not linked",
                      example={
                          "code": 400,
                          "message": "Item and Tag are not linked, nothing was changed",
                          "status": "Bad Request"
                      })
    @blp.alt_response(404, description="Returned if either item or tag were not found",
                      example={
                          "code": 404,
                          "status": "Not Found"
                      })
    @blp.alt_response(500, description="Returned if there is an error in the database")
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        if tag not in item.tags:
            abort(400, message="Item and Tag are not linked, nothing was changed")
        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return {"message": "Successfuly unlinked", "item": item, "tag": tag}


@blp.route("/tag")
class Tag(MethodView):
    @blp.response(200, TagSchema(many=True), description="Returns all tags in the database")
    def get(self):
        return TagModel.query.all()
