from flask import Flask, request
from typing import List

app = Flask(__name__)


class Item:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def dict(self):
        return {
            "name": self.name,
            "price": self.price
        }


class Store:
    def __init__(self, name: str, items: List[Item]):
        self.name = name
        self.items = items

    def dict(self):
        return {
            "name": self.name,
            "items": [item.dict() for item in self.items]
        }

    def list_items(self):
        return [item.dict() for item in self.items]

    def add_item(self, item: Item):
        self.items.append(item)

    def add_items(self, items: List[Item]):
        for item in items:
            self.items.append(item)


items1 = [Item("Chair", 15.99)]
store1 = Store("My Store", items1)
stores = [store1]


@app.get("/stores")  # http://127.0.0.1:5000/stores
def get_stores():
    return {"stores": [store.dict() for store in stores]}


@app.post("/store")
def add_store():
    req = request.get_json()
    new_store = Store(req["name"], [])
    stores.append(new_store)
    return new_store.dict(), 201


@app.post("/store/<string:store_name>/item")
def add_item_to_store(store_name):
    req = request.get_json()
    for store in stores:
        if store.name == store_name:
            if isinstance(req, dict):
                store.add_item(Item(req["name"], req["price"]))
                return store.dict(), 201
            else:
                return {"message": "Invalid request, expected object"}, 400
    return {"message": f"Store {store_name} not found"}, 404


@app.post("/store/<string:store_name>/items")
def add_items_to_store(store_name):
    req = request.get_json()
    for store in stores:
        if store.name == store_name:
            if isinstance(req, list):
                new_items = [Item(dict_item["name"], dict_item["price"]) for dict_item in req]
                store.add_items(new_items)
                return store.dict(), 201
            else:
                return {"message": "Invalid request, expected list"}, 400
    return {"message": f"Store {store_name} not found"}, 404


@app.get("/store/<string:store_name>")  # http://127.0.0.1:5000/store/My%20Store
def get_store(store_name):
    for store in stores:
        if store_name == store.name:
            return store.dict()
    return {"message": f"Store {store_name} not found"}, 404


@app.get("/store/<string:store_name>/items")  # http://127.0.0.1:5000/store/My%20Store/items
def get_items_from_store(store_name):
    for store in stores:
        if store_name == store.name:
            return {"items": store.list_items()}
    return {"message": f"Store {store_name} not found"}, 404
