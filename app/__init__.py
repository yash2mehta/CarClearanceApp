from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app(config=None):
    app = Flask(__name__)
    
    # Configure the app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///immigration.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'uploads'
    
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    
    # Initialize API
    api = Api(app, version="1.0", title="Immigration API", 
             description="A simple API for managing immigration workflows")
    
    # Import and register routes
    from app.api.routes import user_routes, vehicle_routes, preset_routes, pass_routes, traveller_routes
    
    # Register namespaces
    api.add_namespace(user_routes.ns_user)
    api.add_namespace(vehicle_routes.ns_vehicle)
    api.add_namespace(preset_routes.ns_preset)
    api.add_namespace(pass_routes.ns_pass)
    api.add_namespace(traveller_routes.ns_traveller)
    
    return app 