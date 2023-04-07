from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import TagModel, StoreModel
from schemas import TagSchema

blp = Blueprint("Tags", __name__, description="Operations on tags")

@blp.route("/store/<string:store_id>/tag")
class TagStoreID(MethodView):
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, req, store_id):
        new_tag = TagModel(**req, store_id=store_id)
        try:
            db.session.add(new_tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message="An error occured")
        return new_tag, 201

    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()


@blp.route("/tag/<string:tag_id>")
class TagID(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        return TagModel.query.get_or_404(tag_id)