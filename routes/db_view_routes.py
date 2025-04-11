from flask import render_template, Blueprint
from models import (
    UserSensitiveInformation, 
    Vehicle, 
    UserVehicle, 
    Pass, 
    PassTraveller, 
    Preset, 
    PresetTraveller, 
    UserTraveller
)

def init_db_view_routes(app):
    db_bp = Blueprint('db', __name__)

    @db_bp.route('/show-tables')
    def show_tables():
        """Display all tables in the database."""
        user_sensitive_data = UserSensitiveInformation.query.all()
        vehicle_data = Vehicle.query.all()
        user_vehicle_data = UserVehicle.query.all()
        pass_data = Pass.query.all()
        pass_traveller_data = PassTraveller.query.all()
        preset_data = Preset.query.all()
        preset_traveller_data = PresetTraveller.query.all()
        user_traveller_data = UserTraveller.query.all()

        return render_template('view_tables.html',
            user_sensitive_data=user_sensitive_data,
            vehicle_data=vehicle_data,
            user_vehicle_data=user_vehicle_data,
            pass_data=pass_data,
            pass_traveller_data=pass_traveller_data,
            preset_data=preset_data,
            preset_traveller_data=preset_traveller_data,
            user_traveller_data=user_traveller_data
        )

    app.register_blueprint(db_bp, url_prefix='/db') 