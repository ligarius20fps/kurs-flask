from flask import Flask, request
from db import stores, items
from uuid import uuid4

app = Flask(__name__)


@app.get("/stores")  # http://127.0.0.1:5000/stores
def get_all_stores():
    return {"stores": list(stores.values())}


@app.get("/items")  # http://127.0.0.1:5000/items
def get_all_items():
    return {"items": list(items.values())}


@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return {"message": f"Store with ID {store_id} not found"}, 404


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return {"message": f"Item with ID {item_id} not found"}, 404


@app.post("/store")
def add_store():
    req = request.get_json()
    store_id = uuid4().hex
    new_store = req | {"store_id": store_id}
    stores[store_id] = new_store
    return new_store, 201


@app.post("/item")
def add_item_to_store():
    req = request.get_json()
    store_id = req["store_id"]
    if store_id not in stores:
        return {"message": f"Store with ID {store_id} not found"}, 404
    item_id = uuid4().hex
    new_item = req | {"item_id": item_id}
    items[item_id] = new_item
    return new_item
