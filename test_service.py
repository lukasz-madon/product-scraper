import unittest
import requests
import json
from service import app, db
from product import Product
import datetime

class TestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/test.db"
        self.app = app.test_client()
        db.create_all()
        self.data = {'code': 'g',
        'description': 'Giulia',
        'designer': 'alice',
        'gender': 'F',
        'image_urls': ['http://www.oxygenboutique.com/GetImage/d',
                       'http://www.oxygenboutique.com/GetImage/d'],
        'last_updated': '2013-07-12 17:25:24',
        'name': 'Giulia Emb',
        'price': 690.0,
        'raw_color': '',
        'sale_discount': 0,
        'source_url': 'http://www.oxygenboutique.com/giulia-em',
        'stock_status': {u'L': 1, u'M': 1, u'S': 3, u'XS': 3},
        'type': 'A'}
        self.data["__type__"] = "Product"

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_products(self):
        prod = Product("a", "b", "des", 34.0, "F", "['h','ht']", "name", "color", 0.0,
                        "sourc_url", "{u'L': 1, u'M': 1, u'S': 3, u'XS': 3}", datetime.datetime.now(), "A")
        db.session.add(prod)
        db.session.commit()
        res = self.app.get("/rest/products/", environ_base={"REMOTE_ADDR": "127.0.0.1"})
        result = json.loads(res.data)
        json_prod = result["result"][0]
        json_prod["__type__"] = "Product"
        assert res.status_code == 200
        assert Product.json_to_product(json_prod) == prod

    def test_get_products_since(self):
        prod = Product("a", "b", "des", 34.0, "F", "['h','ht']", "name", "color", 0.0,
                        "sourc_url", "{u'L': 1, u'M': 1, u'S': 3, u'XS': 3}", datetime.datetime(2013, 7, 12, 20, 1, 1, 1), "A")
        db.session.add(prod)
        db.session.commit()
        res = self.app.get("/rest/products/?since=2010-1-1", environ_base={"REMOTE_ADDR": "127.0.0.1"})
        result = json.loads(res.data)
        json_prod = result["result"][0]
        json_prod["__type__"] = "Product"
        assert res.status_code == 200
        assert Product.json_to_product(json_prod) == prod     
    
    def test_invalid_date_for_since_param(self):
        res = self.app.get("/rest/products/?since=xxxx-1-1", environ_base={"REMOTE_ADDR": "127.0.0.1"})
        result = json.loads(res.data)
        result_value = result["result"]
        assert res.status_code == 200
        assert result_value == "invalid time" 

    def test_rest_service_with_adding_one_product(self):
        res = self.app.put("/rest/products/", data=json.dumps(self.data),
                       environ_base={"REMOTE_ADDR": "127.0.0.1"}, content_type="application/json")
        assert res.status_code == 200
        assert res.data == '{"result": "added"}'

    def test_if_product_is_in_db(self):
        res = self.app.put("/rest/products/", data=json.dumps(self.data),
                       environ_base={"REMOTE_ADDR": "127.0.0.1"}, content_type="application/json")
        assert res.status_code == 200
        assert Product.json_to_product(self.data) == Product.query.get(self.data["code"])        

if __name__ == "__main__":
    unittest.main()