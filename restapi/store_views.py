import logging
from flask import render_template, request, jsonify
from flask_smorest import Blueprint, abort
from jinja2 import TemplateNotFound

from restapi.db import stores_details, items_details
from restapi.constants.status_codes import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_201_CREATED,\
                                        HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST

import uuid

stores_page = Blueprint("stores_page", __name__, template_folder="templates", url_prefix="/stores")

@stores_page.route("/")
def show_stores():
    try:
        template_name = "stores_home.html"
        page_title = "Stores Homepage"
        logging.info(f"Attempting to render template: {template_name}")
        welcome_note = "Welcome to the stores homepage"
        return render_template("stores_templates/stores_home.html", page_title=page_title, welcome_note=welcome_note) 
    except TemplateNotFound:
        logging.error(f"Template not found: {template_name}")
        abort(404, description="Template restapi/templates/stores_templates/home.html not found")

###################### Stores Details ####################################

@stores_page.get("/store")
def get_all_stores():
    return {"stores" : list(stores_details.values())}, HTTP_200_OK

@stores_page.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores_details[store_id], HTTP_200_OK
    except KeyError:
        abort(404, message="store not found")

@stores_page.post("/store")
def create_store():
    store_data = request.get_json()

    if "name" not in store_data:
        abort(404,
              message="Bad request. name must be included in JSON payload")
        
    if any(store_data["name"]==store["name"] for store in stores_details.values()):
        abort(404, message="store already existed")

    store_id = uuid.uuid4().hex
    new_Store = {**store_data, "id":store_id}
    stores_details[store_id] = new_Store

    return new_Store, HTTP_201_CREATED

@stores_page.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores_details[store_id]
        return {"message": f"store with id {store_id} deleted"}
    except KeyError:
        abort(404, message="store doesn't exist")

@stores_page.put("/store/<string:store_id>")
def update_store(store_id):
    store_data = request.get_json()
    if ("name" not in store_data):
        abort(404,
               message="Bad reqeust. ensure price, name, store_id are included in json payload.")
    try:
        store = stores_details[store_id]
        store |= store_data
        return store
    except KeyError:
        abort(404, "store doesn't exist")

###################### Items Details ####################################

@stores_page.get("/item")
def get_all_items():
    return {"items" : list(items_details.values())}, HTTP_200_OK

@stores_page.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items_details[item_id], HTTP_200_OK
    except KeyError:
        abort(404, message="item not found")

@stores_page.post("/item")
def create_item():
    item_data = request.get_json()

    if ("name" not in item_data
        or "price" not in item_data
        or "store_id" not in item_data):
        
        abort(404,
               message="Bad reqeust. ensure price, name, store_id are included in json payload.")
    
    if any(item_data["name"]==item["name"] for item in items_details.values()):
        abort(404, message="item already existed")

    if item_data["store_id"] not in stores_details:
        abort(404, message="store not found")
    
    item_id = uuid.uuid4().hex
    new_item = {**item_data, "id":item_id}
    items_details[item_id] = new_item

    return new_item, HTTP_201_CREATED

@stores_page.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items_details[item_id]
        return {"message": f"item with id {item_id} deleted"}
    except KeyError:
        abort(404, message="item doesn't exist")

@stores_page.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()

    if ("price" not in item_data
        or "name" not in item_data
        or "store_id" not in item_data):
        
        abort(404,
               message="Bad reqeust. ensure price, name, store_id are included in json payload.")
    
    try:
        item = items_details[item_id]
        item |= item_data # inplace replacement or new dictinary update operator
        return item
    except KeyError:
        abort(404, message="item not found")

    