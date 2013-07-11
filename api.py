from flask import request
from service import app
from product import Product

@app.route("/rest/products/", methods=["GET", "PUT"])
def products():
    if request.method == "PUT":
        return add_products()
    else:
        return get_products()

def get_products():
    all_products = [str(elem) for elem in Product.query.all()]
    return "".join(all_products)

def add_products():
    return '{"result": "added"}'
