from mock_data import insert_mock_data
from api_instance import app, api, db
from models import UserSensitiveInformation, Vehicle, UserVehicle, Pass, PassTraveller, Preset, PresetTraveller, UserTraveller

# Import route initializers
from routes.vehicle_routes import init_vehicle_routes
from routes.user_routes import init_user_routes
from routes.preset_routes import init_preset_routes
from routes.pass_routes import init_pass_routes
from routes.traveller_routes import init_traveller_routes
from routes.db_view_routes import init_db_view_routes

# Initialize routes
init_vehicle_routes(api)
init_user_routes(api)
init_preset_routes(api)
init_pass_routes(api)
init_traveller_routes(api)
init_db_view_routes(app)

if __name__ == '__main__':
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()
        insert_mock_data()
    app.run(debug=True, host='0.0.0.0', port=5000) 