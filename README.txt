REST service that will provide developers with oxygenboutique.com products in a structured format (JSON)

Deps (can be downloaded with pip)
- Flask
- Flask-SQLAlchemy
- Scrapy
- requests

to run:
./start_service
./spider

http://127.0.0.1:5000/rest/products/
{"result": [{"code": ...
http://127.0.0.1:5000/rest/products/?since=2013-06-11
{"result": [{"code": ...
http://127.0.0.1:5000/rest/products/?since=2017-06-11
{"result": []}
http://127.0.0.1:5000/rest/products/?since=2017-06-ss
{"result": "invalid time"}