from flask import request
from service import app, db
from product import Product


@app.route("/rest/products/", methods=["GET", "PUT"])
def products():
	if request.method == "PUT" and request.remote_addr == "127.0.0.1":
		return add_products(request.get_json())
	else:
		return get_products()

def get_products():
	all_products = Product.query.all()
	result = str([prod.to_json() for prod in all_products])
	return '{"result": ' + result +'}' 

def add_products(product):
	prod = json_to_product(product)
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

def json_to_product(prod):
	if "__type__" in prod and prod["__type__"] == "Product":
		image_urls = str(prod["image_urls"])
		return Product(prod["code"], prod["description"], prod["designer"], prod["price"],
						prod["gender"], image_urls, prod["name"], prod["raw_color"],
						prod["sale_discount"], prod["source_url"], str(prod["stock_status"]),
						prod["last_updated"], prod["type"])
						