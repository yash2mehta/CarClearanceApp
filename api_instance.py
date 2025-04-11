from flask_restx import Api
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import API_VERSION, API_TITLE, API_DESCRIPTION, SQLALCHEMY_DATABASE_URI
from db_instance import db

# Create Flask app
app = Flask(__name__)
CORS(app)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create API instance
api = Api(
    app,
    version=API_VERSION,
    title=API_TITLE,
    description=API_DESCRIPTION
) 