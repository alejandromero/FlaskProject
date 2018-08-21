from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("config.DebugDBConfig")
db = SQLAlchemy(app)

from app.jinja_functions import *
from app.routes import *