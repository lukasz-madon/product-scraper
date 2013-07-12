from flask import request
from service import app, db
from product import Product
from datetime import datetime, timedelta


@app.route("/rest/products/", methods=["GET", "PUT"])
def products():
    if request.method == "PUT" and request.remote_addr == "127.0.0.1":
        return add_products(request.get_json())
    else:
        if request.args:
            return get_products(request.args.get("since"))
        else:
            return get_products(None)


def get_products(since):
    all_products = []
    if since is None:
        all_products = Product.query.all()
    else:
        try:
            s = datetime.strptime(since, "%Y-%m-%d")
        except ValueError:
            return '{"result": "invalid time"}'
        all_products = Product.query.filter(Product.last_updated >= s)
    old_date = datetime.now() - timedelta(days=30)
    # filter old - doing it every get is an overkill, but number of items is
    # less than 1000
    res = "".join([prod.to_json()
                  for prod in all_products if prod.last_updated >= old_date])
    return '{"result": [' + res + ']}'


def add_products(product):
    prod = Product.json_to_product(product)
    prod_ent = Product.query.get(prod.code)
    if prod_ent:
        prod_ent.description = prod.description
        prod_ent.designer = prod.designer
        prod_ent.price = prod.price
        prod_ent.gender = prod.gender
        prod_ent.image_urls = prod.image_urls
        prod_ent.name = prod.name
        prod_ent.raw_color = prod.raw_color
        prod_ent.sale_discount = prod.sale_discount
        prod_ent.source_url = prod.source_url
        prod_ent.stock_status = prod.stock_status
        prod_ent.last_updated = prod.last_updated
        prod_ent.type = prod.type
        db.session.commit()
        return '{"result": "updated"}'
    else:
        db.session.add(prod)
        db.session.commit()
        return '{"result": "added"}'
