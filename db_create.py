from service import db
from product import Product

db.create_all()

#prod1 = Product("p-1587-lexi-tee", "a", "bb", 2.0, "M",  """['http://oxygenboutique.com/i.jpg','http://oxygenboutique.com/2.jpg',""",
#                "smy", "navy", 0.2, """http://oxygenboutique.com/src.jpg""", "{'XS': 3}", "2013-07-05 10:19:21", "A")

#db.session.add(prod1)
#db.session.commit()

#print Product.query.all()