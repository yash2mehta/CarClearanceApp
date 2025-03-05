from datetime import datetime
from db_instance import db

# Define the database models
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone_number = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class UserSensitiveInformation(db.Model):
    user_auth_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False, unique=True)  # 1-to-1 with User
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), nullable=True)  # Nullable field
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    passport_issuing_country = db.Column(db.String(255), nullable=False)
    passport_number = db.Column(db.String(20), nullable=False, unique=True)  # Passport number is the unique identifier, along with user id 
    passport_expiry = db.Column(db.DateTime, nullable=False)
    fingerprint_hash = db.Column(db.String(255), nullable=True)  # Store hashed fingerprint - used for biometric verification

class Vehicle(db.Model):
    vehicle_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vehicle_number = db.Column(db.String(20), nullable=False, unique=True)

class UserVehicle(db.Model):
    user_vehicle_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.vehicle_id'), nullable=False)
    user_vehicle_name = db.Column(db.String(100), nullable=False)

class Location(db.Model):
    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)

class Pass(db.Model):
    pass_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.vehicle_id'), nullable=False)
    creator_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    creation_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    expiry_datetime = db.Column(db.DateTime, nullable=False)
    pass_date = db.Column(db.Date, nullable=False)
    origin_id = db.Column(db.Integer, db.ForeignKey('location.location_id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('location.location_id'), nullable=False)
    pass_utilized = db.Column(db.Boolean, nullable=False, default=False)


class PassTraveller(db.Model):
    pass_traveller_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pass_id = db.Column(db.Integer, db.ForeignKey('pass.pass_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

class Preset(db.Model):
    preset_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    preset_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

class PresetTraveller(db.Model):
    preset_traveller_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    preset_id = db.Column(db.Integer, db.ForeignKey('preset.preset_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
