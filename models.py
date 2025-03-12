from datetime import datetime
from db_instance import db

# assumption: people who wants to travel are already registered in the app

'''
# for login, but now firebase handles this, KIV whether we still need this
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True) # autonumbering primary key
    email = db.Column(db.String(255), nullable=False, unique=True) # unique email
    phone_number = db.Column(db.String(20), nullable=False) # phone number
    password_hash = db.Column(db.String(255), nullable=False) # hashed password
'''

# for the person who is logging in, NOT traveller details
class UserSensitiveInformation(db.Model):
    __tablename__ = 'user_sensitive_information'  # Table name
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), nullable=True)  # Optional, Nullable field
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    passport_issuing_country = db.Column(db.String(255), nullable=False) # "nationality"
    passport_number = db.Column(db.String(20), nullable=False, unique=True) # Passport number is the unique identifier, along with user id 
    passport_expiry = db.Column(db.Date, nullable=False)

# db for all vehicles
class Vehicle(db.Model):
    vehicle_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vehicle_number = db.Column(db.String(20), nullable=False, unique=True)

# database for a specific user's vehicle
class UserVehicle(db.Model):
    user_vehicle_id = db.Column(db.Integer, primary_key=True, autoincrement=True) # Autonumber
    user_id = db.Column(db.Integer, db.ForeignKey(UserSensitiveInformation.user_id), nullable=False) # get the user we are referring to
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.vehicle_id'), nullable=False) # get the vehicle we are referring to
    user_vehicle_model = db.Column(db.String(100), nullable=False)

'''
# database for location (in case IDEMIA wants to expand to other countries)
class Location(db.Model):
    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
'''

# passes created by users
class Pass(db.Model):
    pass_id = db.Column(db.Integer, primary_key=True, autoincrement=True) # autonumber
    # vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.vehicle_id'), nullable=False) # users no longer need to put vehicles in their passes
    creator_user_id = db.Column(db.Integer, db.ForeignKey(UserSensitiveInformation.user_id), nullable=False) # get the user who created the pass
    # creation_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # when the pass was created
    pass_date = db.Column(db.DateTime, nullable=False) # date of pass user wants to create, expiry date is 24h from this date (logic implemented in react app), this will be the date used for history page
    expiry_datetime = db.Column(db.DateTime, nullable=False) 
    # origin_id = db.Column(db.Integer, db.ForeignKey('location.location_id'), nullable=False)
    # destination_id = db.Column(db.Integer, db.ForeignKey('location.location_id'), nullable=False)
    pass_utilized = db.Column(db.Boolean, nullable=False, default=False) # whether the travellers have gone through checkpoint (T/F)


# stores mapping info between pass and traveller
class PassTraveller(db.Model):
    pass_traveller_id = db.Column(db.Integer, primary_key=True, autoincrement=True) # autonumber
    pass_id = db.Column(db.Integer, db.ForeignKey('pass.pass_id'), nullable=False) # the specific pass user created
    user_id = db.Column(db.Integer, db.ForeignKey(UserSensitiveInformation.user_id), nullable=False) # user id of travellers in the pass // pull the users data from class UserSensitiveInformation table

# stores preset info
class Preset(db.Model):
    preset_id = db.Column(db.Integer, primary_key=True, autoincrement=True) # autonumber
    preset_name = db.Column(db.String(100), nullable=False) # name of the preset
    user_id = db.Column(db.Integer, db.ForeignKey(UserSensitiveInformation.user_id), nullable=False) # the user account that we are referring to, for all the presets he created

# stores all the travellers in the preset
class PresetTraveller(db.Model):
    preset_traveller_id = db.Column(db.Integer, primary_key=True, autoincrement=True) # autonumber
    preset_id = db.Column(db.Integer, db.ForeignKey('preset.preset_id'), nullable=False) # gets the preset
    user_id = db.Column(db.Integer, db.ForeignKey(UserSensitiveInformation.user_id), nullable=False) # references travelers in the pass, and gets the information from UserSensitiveInformation table
    
# Stores all travelers that the user has added (doesn't need to be related to preset/pass)
class UserTraveller(db.Model):
    user_traveller_id = db.Column(db.Integer, primary_key=True, autoincrement=True) # autonumber
    creator_user_id = db.Column(db.Integer, db.ForeignKey(UserSensitiveInformation.user_id), nullable=False) # User id of the particular user who adds travellers linked to their account
    traveller_id = db.Column(db.Integer, db.ForeignKey(UserSensitiveInformation.user_id), nullable=False) # User id of the travellers that have been added

