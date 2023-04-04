from flask import Flask, request
from db import stores, items
from uuid import uuid4
from flask_smorest import abort

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
        abort(404, message=f"Store with ID {store_id} not found")


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message=f"Item with ID {item_id} not found")


@app.post("/store")
def add_store():
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


@app.post("/item")
def add_item_to_store():
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
    return new_item


@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted"}
    except KeyError:
        abort(404, message=f"Item not found")
