REST service that will provide developers with oxygenboutique.com products in a structured format (JSON)

Tested with Python 2.7 (32 bit)

Deps (can be downloaded with pip)
- Flask
- Flask-SQLAlchemy
- Scrapy
- requests

to run:
python start_service.py {prod,dev}
python spider.py

to test:
python test_service.py

Example output:
http://127.0.0.1:5000/rest/products/
{"result": [{"code": ...
http://127.0.0.1:5000/rest/products/?since=2013-06-11
{"result": [{"code": ...
http://127.0.0.1:5000/rest/products/?since=2017-06-11
{"result": []}
http://127.0.0.1:5000/rest/products/?since=2017-06-ss
{"result": "invalid time"}