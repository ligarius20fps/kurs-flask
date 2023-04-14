from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required
from db import db
from schemas import StoreSchema
from models import StoreModel

blp = Blueprint("Stores", __name__, description="Operations on stores")


@blp.route("/store")
class Store(MethodView):
    @jwt_required()
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema,description="Adds a store with a unique name")
    @blp.alt_response(400, description="Returned if store name already exists in the database",
                      example={
                        "code": 400,
                        "message": "The store already exists",
                        "status": "Bad Request"
                        })
    @blp.alt_response(500, description="Returned if there is an error in the database")
    def post(self, req):
        new_store = StoreModel(**req)
        try:
            db.session.add(new_store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="The store already exists")
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return new_store, 201

    @blp.response(200, StoreSchema(many=True), description="Returns all stores in the database")
    def get(self):  # http://127.0.0.1:5000/store
        return StoreModel.query.all()


@blp.route("/store/<int:store_id>")
class StoreID(MethodView):
    @blp.response(200, StoreSchema, description="Returns a store with provided ID")
    @blp.alt_response(404, description="Returned if no store found with such ID",
                      example={
                        "code": 404,
                        "status": "Not Found"
                    })
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    @jwt_required(fresh=True)
    @blp.response(200, description="Deletes a store with provided ID", example={"message": "Store successfully deleted"})
    @blp.alt_response(404, description="Returned if no store found with such ID",
                      example={
                          "code": 404,
                          "status": "Not Found"
                      })
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        try:
            db.session.delete(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Can't delete a store with items or tags associated with it")
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return {"message": "Store successfully deleted"}
