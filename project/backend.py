#import modules from flask for api
from flask import *
from flask_httpauth import HTTPBasicAuth

#variable app is app name
app = Flask(__name__)



#authentication method, flask_httpauth creates a method to require
#authentication for flask urls
auth = HTTPBasicAuth()
users = {
    "clientuser": "samplepassword"
}
#username and password required for viewing and modifying database
@auth.get_password
def authenticate(u):
    if u in users:
        return users.get(u)
    return None

#message for wrong username/password
@auth.error_handler
def unauthorized():
    return make_response(jsonify({"error": "Access Denied"}))

#items list, items are stored as a 2d array
items = [
    {
        "id": 1,
        "name": u"Barite",
        "info": u">90% BaSO4", 
        "unavailable": False
    },
    {
        "id": 2,
        "name": u"Silica Sand",
        "info": u">99.5% SiO2", 
        "unavailable": False
    }
]

#orders list, a separate 2d array
#contains an example
orders = [
    {
        "id": 1,
        "item": u"the item being ordered",
        "info": u"This purpose of this order is x. details about the client is y."
    }
]

#urls defined by app.route and different calls to that url

#GET calls
#calling get to /items gets list of items
@app.route("/items", methods=["GET"])
def get_items():
    x = {"items": items}
    return jsonify(x)

#calling get to /orders gets list of orders
@app.route("/orders", methods=["GET"])
def get_orders():
    return jsonify({"orders": orders})

#calling get for specific item
#ex. calling get to /items/2 gets the second item (with id of 2)
@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    #for each item, if the id is the called id, return the item
    item = [item for item in items if item["id"] == item_id]
    return jsonify({"item": item[0]})

#create an item, must authenticate
@app.route("/items", methods=["POST"])
@auth.login_required
def create_item():
    #format of item created by method
    item = {
        "id": items[-1]["id"] + 1,
        "name": request.json.get("name", ""),
        "info": request.json.get("info", ""),
        "unavailable": False
    }
    #add item to items array and return item
    items.append(item)
    return jsonify({"item": item})

#create an order
@app.route("/orders", methods=["POST"])
def create_order():
    #similar to create item
    order = {
        "id": orders[-1]["id"] + 1,
        "item": request.json.get("item", ""),
        "info": request.json.get("info", ""),
    }
    #add item to items array and return item
    orders.append(order)
    return jsonify({"order": order})

#modify items, must authenticate
@app.route("/items/<int:item_id>", methods=["PUT"])
@auth.login_required
def modify_item(item_id):
    item = [item for item in items if item["id"] == item_id]
    item[0]["name"] = request.json.get("name", item[0]["name"])
    item[0]["info"] = request.json.get("info", item[0]["info"])
    item[0]["unavailable"] = request.json.get("unavailable", item[0]["unavailable"])
    return jsonify({"item": item[0]})

#delete an item, must autheticate
@app.route("/items/<int:item_id>", methods=["DELETE"])
@auth.login_required
def delete_item(item_id):
    item = [item for item in items if item["id"] == item_id]
    items.remove(item[0])
    return jsonify({"deleted": True})


#run app
if __name__ == "__main__":
    app.run(debug=True)
