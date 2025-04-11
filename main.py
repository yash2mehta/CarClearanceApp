from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI, API_VERSION, API_TITLE, API_DESCRIPTION
from db_instance import db
from mock_data import insert_mock_data

# Import route initializers
from routes.vehicle_routes import init_vehicle_routes
from routes.user_routes import init_user_routes
from routes.preset_routes import init_preset_routes
from routes.pass_routes import init_pass_routes
from routes.traveller_routes import init_traveller_routes

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    db.init_app(app)
    
    # Initialize API
    api = Api(app, 
              version=API_VERSION, 
              title=API_TITLE, 
              description=API_DESCRIPTION)
    
    # Initialize all routes
    init_vehicle_routes(api)
    init_user_routes(api)
    init_preset_routes(api)
    init_pass_routes(api)
    init_traveller_routes(api)
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    # Initialize database and insert mock data
    with app.app_context():
        db.drop_all()
        db.create_all()
        insert_mock_data()
    
    app.run(debug=True, host='0.0.0.0', port=5000) 