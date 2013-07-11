from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os.path

basedir = os.path.abspath(os.path.dirname(__file__))
db_file = os.path.join(basedir, "data/products.db")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_file
db = SQLAlchemy(app)

import api

db.create_all()