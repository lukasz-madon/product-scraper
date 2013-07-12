from service import db
import ast
import json
from datetime import datetime


class Product(db.Model):

    """represents a scraped product"""
    code = db.Column(
        db.String(20), primary_key=True, nullable=False, autoincrement=False)
    description = db.Column(db.String(300))
    designer = db.Column(db.String(50))
    price = db.Column(db.Float)
    gender = db.Column(db.String(1))
    image_urls = db.Column(db.String(400))
    name = db.Column(db.String(30))
    raw_color = db.Column(db.String(15))
    sale_discount = db.Column(db.Float)
    source_url = db.Column(db.String(60))
    stock_status = db.Column(db.String(40))
    last_updated = db.Column(db.DateTime)
    type = db.Column(db.String(1))

    def __init__(self, code, description, designer, price, gender, image_urls,
                 name, raw_color, sale_discount, source_url, stock_status,
                 last_updated, type):
        self.code = code
        self.description = description
        self.designer = designer
        self.price = price
        self.gender = gender
        self.image_urls = image_urls
        self.name = name
        self.raw_color = raw_color
        self.sale_discount = sale_discount
        self.source_url = source_url
        self.stock_status = stock_status
        self.last_updated = last_updated
        self.type = type
        
    def __eq__(self, other): 
        return self.code == other.code

    def to_json(self):
        prod = {}
        prod["code"] = self.code
        prod["description"] = self.description
        prod["designer"] = self.designer
        prod["price"] = self.price
        prod["gender"] = self.gender
        prod["name"] = self.name
        prod["image_urls"] = ast.literal_eval(self.image_urls)
        prod["raw_color"] = self.raw_color
        prod["sale_discount"] = self.sale_discount
        prod["source_url"] = self.source_url
        prod["stock_status"] = ast.literal_eval(self.stock_status)
        prod["last_updated"] = self.last_updated.strftime("%Y-%m-%d %H:%M:%S")
        prod["type"] = self.type
        return json.dumps(prod)

    @staticmethod
    def json_to_product(prod):
        if "__type__" in prod and prod["__type__"] == "Product":
            image_urls = str(prod["image_urls"])
            stock_status = str(prod["stock_status"])
            last_updated = datetime.strptime(prod["last_updated"], "%Y-%m-%d %H:%M:%S")
            return Product(prod["code"], prod["description"], prod["designer"],
                            prod["price"], prod["gender"], image_urls, prod["name"],
                            prod["raw_color"],prod["sale_discount"], prod["source_url"],
                            stock_status, last_updated, prod["type"])
