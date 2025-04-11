from datetime import datetime
from db_instance import db


class UserSensitiveInformation(db.Model):
    __tablename__ = 'user_sensitive_information'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    passport_issuing_country = db.Column(db.String(255), nullable=False)
    passport_number = db.Column(db.String(20), nullable=False, unique=True)
    passport_expiry = db.Column(db.Date, nullable=False)


class Vehicle(db.Model):
    vehicle_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vehicle_number = db.Column(db.String(20), nullable=False, unique=True)


class UserVehicle(db.Model):
    user_vehicle_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(UserSensitiveInformation.user_id), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.vehicle_id'), nullable=False)
    user_vehicle_model = db.Column(db.String(100), nullable=False)



class Pass(db.Model):
    pass_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator_user_id = db.Column(db.Integer, db.ForeignKey(UserSensitiveInformation.user_id), nullable=False)
    pass_date = db.Column(db.DateTime, nullable=False)
    expiry_datetime = db.Column(db.DateTime, nullable=False) 
    pass_utilized = db.Column(db.Boolean, nullable=False, default=False)



class PassTraveller(db.Model):
    pass_traveller_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pass_id = db.Column(db.Integer, db.ForeignKey('pass.pass_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(UserSensitiveInformation.user_id), nullable=False)


class Preset(db.Model):
    preset_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    preset_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(UserSensitiveInformation.user_id), nullable=False)


class PresetTraveller(db.Model):
    preset_traveller_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    preset_id = db.Column(db.Integer, db.ForeignKey('preset.preset_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(UserSensitiveInformation.user_id), nullable=False)
    

class UserTraveller(db.Model):
    user_traveller_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator_user_id = db.Column(db.Integer, db.ForeignKey(UserSensitiveInformation.user_id), nullable=False)
    traveller_id = db.Column(db.Integer, db.ForeignKey(UserSensitiveInformation.user_id), nullable=False)

