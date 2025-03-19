# Importing required modules
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, jsonify
import os
import requests
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from pprint import pprint
from flask_cors import CORS # Include CORS Requests
from datetime import datetime, timedelta

# Import the database instance
from db_instance import db

# Immigration Checkpoint Workflow Logic
from immigration_logic import immigration_walkthrough

from models import UserSensitiveInformation, Vehicle, UserVehicle, Preset, PresetTraveller, Pass, PassTraveller, UserTraveller

# Import mock_data function
from mock_data import insert_mock_data

# Initializing Flask App
app = Flask(__name__)
CORS(app)  # Enable CORS for React Native requests

# Configuration
UPLOAD_FOLDER = 'uploads' # Directory where uploaded images will be saved
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER # Use Upload_Folder for file uploads
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///immigration.db' # SQLite Database URI for local testing
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
TOKEN = "210ed0449ee06e8d9bcee4a67c742814e4e7366e" # This is the PlateRecognizer API Token
API_URL = "https://api.platerecognizer.com/v1/plate-reader/" # This is the PlateRecognizer API Url


# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize SQLAlchemy for the Flask app
db.init_app(app)


# Defines the route for Homepage (consisting of Image Upload)
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    
    # POST Method is called
    if request.method == 'POST':

        # If no file uploaded, reload current page
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        
        # If the filename is empty, reload current page 
        if file.filename == '':
            return redirect(request.url)
        
        # If file was correctly uploaded so far
        if file:

            # Sanitize the filename
            filename = secure_filename(file.filename)

            # Save uploaded file to specific path/folder
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Process the image using PlateRecognizer API
            license_plate = recognize_license_plate(file_path, TOKEN)

            if "Error" in license_plate or license_plate == "No license plate detected.":
                return render_template('upload.html', filename=filename, license_plate=license_plate)
            
            # Start the database logic process
            immigration_result = immigration_walkthrough(license_plate)
            
            return render_template('upload.html', filename=filename, license_plate=license_plate, immigration_result=immigration_result)

    
    # GET Method is called
    else:
        return render_template('upload.html')

# Define the route for Mask of Vehicular Guidance System
@app.route('/vehicular-guidance-system', methods=['GET', 'POST'])
def vehicular_guidance_system():
    
    # POST Method is called
    if request.method == 'POST':

        # If no file uploaded, reload current page
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        
        # If the filename is empty, reload current page 
        if file.filename == '':
            return redirect(request.url)
        
        # If file was correctly uploaded so far
        if file:

            # Sanitize the filename
            filename = secure_filename(file.filename)

            # Save uploaded file to specific path/folder
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Process the image using PlateRecognizer API
            #TODO - Need to change the PlateRecognizer API and include Make, Model and Color to be returned and validation for that
            license_plate = recognize_license_plate(file_path, TOKEN)
            make = "make"
            model = "model"
            color = "color"
            error_messages = [] # List of error messages to be stored for license plate, make, model and color

            # The vehicular data in json format
            vehicular_data = {
                "license_plate": None,
                "make": None,
                "model": None,
                "color": None
            }

            # --- LICENSE PLATE ---
            if "Error" in license_plate or license_plate == "No license plate detected.":
                error_messages.append("No license plate detected")
                vehicular_data["license_plate"] = None
            else:
                vehicular_data["license_plate"] = license_plate

            # --- MAKE ---
            if "Error" in make or make == "No make detected.":
                error_messages.append("No make detected")
                vehicular_data["make"] = None
            else:
                vehicular_data["make"] = make

            # --- MODEL ---
            if "Error" in model or model == "No model detected.":
                error_messages.append("No model detected")
                vehicular_data["model"] = None
            else:
                vehicular_data["model"] = model

            # --- COLOR ---
            if "Error" in color or color == "No color detected.":
                error_messages.append("No color detected")
                vehicular_data["color"] = None
            else:
                vehicular_data["color"] = color


            # Determine overall status
            if error_messages:
                status = "failed"
                message = " | ".join(error_messages)  # Join all errors into one string
            else:
                status = "success"
                message = "All fields recognized successfully"

            vehicular_guidance_system_result = {
                "status": status,
                "message": message,
                **vehicular_data  # unpacking the vehicular data dictionary with recognized data
            }

            return render_template(
                'vehicular_guidance_system.html',
                filename = filename,
                vehicular_guidance_system_result = vehicular_guidance_system_result
            )
    
    # GET Method is called
    else:
        return render_template('vehicular_guidance_system.html')



@app.route('/api/users/<int:user_id>/vehicles', methods=['POST'])
def add_vehicle_to_user(user_id):

    # 1. Check if user exists
    user = UserSensitiveInformation.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # 2. Parse JSON from request
    data = request.get_json(force=True)
    vehicle_number = data.get('vehicle_number')
    user_vehicle_model = data.get('user_vehicle_model') # Name user has assigned to the vehicle
    
    # If vehicle number or user vehicle name is not mentioned in incoming JSON, throw error
    if not vehicle_number:
        return jsonify({"error": "Missing vehicle_number"}), 400
    
    # 3. Check if the vehicle (by plate number) already exists
    vehicle = Vehicle.query.filter_by(vehicle_number=vehicle_number).first()
    if not vehicle:

        # Create a new vehicle record if none found
        vehicle = Vehicle(vehicle_number=vehicle_number)
        db.session.add(vehicle)
        db.session.commit()

    # 5. Create a new UserVehicle link
    user_vehicle = UserVehicle(
        user_id=user_id,
        vehicle_id=vehicle.vehicle_id,
    )

    db.session.add(user_vehicle)
    db.session.commit()
    
    return jsonify({
        "message": "Vehicle added to user successfully",
        "user_vehicle": {
            "user_id": user_id,
            "vehicle_id": vehicle.vehicle_id,
            "vehicle_number": vehicle.vehicle_number
        }
    }), 201


# Function to recognize license plate using PlateRecognizer API
def recognize_license_plate(image_path, token):

    # Create headers dictionary for authentication
    headers = {
        "Authorization": f"Token {token}"
    }

    with open(image_path, "rb") as fp:

        # Send request to Plate Recognizer
        response = requests.post(API_URL, headers=headers, files={"upload": fp})
        
        # If request was successful
        if response.status_code == 200 or response.status_code == 201:
            
            data = response.json()
            if data['results']:
                
                # Extract license plate from the response
                return data['results'][0]['plate']
            
            else:
                return "No license plate detected."
        
        else:
            return f"Error: {response.status_code}, {response.text}"

@app.route('/api/users/<int:user_id>/vehicles', methods=['GET'])
def get_user_vehicles(user_id):

    # 1. Make sure the user exists
    user = UserSensitiveInformation.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # 2. Join UserVehicle and Vehicle to retrieve user-vehicle pairs
    user_vehicles = (
        db.session.query(UserVehicle, Vehicle)
        .join(Vehicle, UserVehicle.vehicle_id == Vehicle.vehicle_id)
        .filter(UserVehicle.user_id == user_id)
        .all()
    )
    # user_vehicles will be a list of tuples: (UserVehicle, Vehicle)
    
    # 3. Build a list of dicts with the info we need
    vehicles_list = []
    for uv, v in user_vehicles:
        vehicles_list.append({
            "user_vehicle_id": uv.user_vehicle_id,
            "user_vehicle_model": uv.user_vehicle_model,
            "vehicle_id": v.vehicle_id,
            "vehicle_number": v.vehicle_number
        })
    
    # 4. Return the JSON response
    return jsonify({
        # "user_id": user_id,
        "vehicles": vehicles_list
    }), 200


# Get all the preset names and passenger count for a user id (used on homepage)
@app.route('/api/users/<int:user_id>/presets_name', methods=['GET'])
def get_user_presets(user_id):
    
    # Check if user exists
    user = UserSensitiveInformation.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Fetch presets for the given user_id
    presets = Preset.query.filter_by(user_id=user_id).all()

    # Convert to JSON format with passenger count
    presets_list = []
    for p in presets:
        # Count number of passengers in the preset
        passenger_count = db.session.query(PresetTraveller).filter_by(preset_id=p.preset_id).count()
        
        presets_list.append({
            "preset_id": p.preset_id,
            "preset_name": p.preset_name,
            "passenger_count": passenger_count  # Add passenger count
        })

    # Return response
    return jsonify({
        "user_id": user_id,
        "presets": presets_list
    }), 200


# Get all the users for a given preset id - not needed now
@app.route('/api/presets/<int:preset_id>/users', methods=['GET'])
def get_preset_users(preset_id):

    # Check if the preset exists
    preset = Preset.query.get(preset_id)
    if not preset:
        return jsonify({"error": "Preset not found"}), 404

    # Join User, PresetTraveller, and UserSensitiveInformation
    users = (
        db.session.query(
            UserSensitiveInformation.user_id, 
            UserSensitiveInformation.first_name, 
            UserSensitiveInformation.middle_name,
            UserSensitiveInformation.last_name
        )
        .join(PresetTraveller, UserSensitiveInformation.user_id == PresetTraveller.user_id)  # Join PresetTraveller to link presets and users
        .filter(PresetTraveller.preset_id == preset_id)
        .all()
    )

    # Convert to JSON-friendly format
    users_list = [
        {"user_id": u.user_id, "first_name": u.first_name, "middle_name": u.middle_name, "last_name": u.last_name}
        for u in users
    ]

    # Return response
    return jsonify({
        "preset_id": preset.preset_id,
        "preset_name": preset.preset_name,
        "users": users_list
    }), 200

# Get preset id, name and users list 
@app.route('/api/users/<int:user_id>/created-presets-with-users', methods=['GET'])
def get_user_created_presets_with_users(user_id):
    
    # Check if the user exists
    user = UserSensitiveInformation.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Fetch presets created by the user
    presets = (
        db.session.query(Preset.preset_id, Preset.preset_name)
        .filter(Preset.user_id == user_id)
        .all()
    )

    # If user hasn't created any presets, return empty list
    if not presets:
        return jsonify({"user_id": user_id, "presets_created": []}), 200

    presets_data = []
    for preset_id, preset_name in presets:
        # Fetch all users associated with the preset
        preset_users = (
            db.session.query(
                UserSensitiveInformation.user_id,
                UserSensitiveInformation.first_name,
                UserSensitiveInformation.middle_name,
                UserSensitiveInformation.last_name,
                UserSensitiveInformation.passport_number
            )
            .join(PresetTraveller, UserSensitiveInformation.user_id == PresetTraveller.user_id)
            .filter(PresetTraveller.preset_id == preset_id)
            .all()
        )

        # Convert users into JSON format
        users_list = [
            {
                "user_id": u.user_id,
                "first_name": u.first_name,
                "middle_name": u.middle_name,
                "last_name": u.last_name,
                "passport_number": u.passport_number
            }
            for u in preset_users
        ]

        presets_data.append({
            "preset_id": preset_id,
            "preset_name": preset_name,
            "users": users_list
        })

    return jsonify({
        "user_id": user_id,
        "presets_created": presets_data
    }), 200

# Create presets
@app.route('/api/presets/create', methods=['POST'])
def create_preset():

    # Extract data from request body
    data = request.get_json()

    preset_name = data.get("preset_name")
    user_id = data.get("user_id")
    travellers = data.get("travellers", [])

    # Validate required fields
    if not preset_name:
        return jsonify({"error": "Preset name is required"}), 400
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    # Check if the user creating the preset exists
    creator = UserSensitiveInformation.query.get(user_id)
    if not creator:
        return jsonify({"error": f"User ID {user_id} not found"}), 404

    # Create the new preset
    new_preset = Preset(preset_name=preset_name, user_id=user_id)
    db.session.add(new_preset)
    db.session.commit()  # Commit to generate preset_id

    preset_id = new_preset.preset_id  # Retrieve the new preset_id

    # List to store successfully added travellers
    travellers_added = []

    # Process each traveller
    for traveller in travellers:
        passport_number = traveller.get("passport_number")
        given_first_name = traveller.get("first_name")
        given_middle_name = traveller.get("middle_name")
        given_last_name = traveller.get("last_name")

        # Find user_id from passport_number
        user_sensitive = UserSensitiveInformation.query.filter_by(passport_number=passport_number).first()
        if not user_sensitive:
            return jsonify({"error": f"Traveller with passport number {passport_number} not found"}), 404

        traveller_user_id = user_sensitive.user_id

        # Add traveller to PresetTraveller table
        preset_traveller = PresetTraveller(preset_id=preset_id, user_id=traveller_user_id)
        db.session.add(preset_traveller)

        # Append to response list, keeping the given names from request
        travellers_added.append({
            "user_id": traveller_user_id,
            "first_name": given_first_name,
            "middle_name": given_middle_name,
            "last_name": given_last_name,
            "passport_number": passport_number
        })

    db.session.commit()  # Commit all travellers

    return jsonify({
        "message": "Preset created successfully",
        "preset_id": preset_id,
        "preset_name": preset_name,
        "created_by_user_id": user_id,
        "travellers_added": travellers_added
    }), 201


@app.route('/api/users/<int:user_id>/passes', methods=['GET'])
def get_user_passes(user_id):

    # Check if the user exists
    user = UserSensitiveInformation.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Fetch all passes created by the user
    passes = (
        db.session.query(
            Pass.pass_id,
            # Pass.vehicle_id,
            Pass.pass_date,
            Pass.expiry_datetime,
            Pass.pass_utilized
        )
        .filter(Pass.creator_user_id == user_id)
        .all()
    )

    passes_list = []
    for p in passes:
        # Fetch all travellers for the given pass
        travellers = (
            db.session.query(
                UserSensitiveInformation.user_id,
                UserSensitiveInformation.first_name,
                UserSensitiveInformation.middle_name,
                UserSensitiveInformation.last_name,
                UserSensitiveInformation.passport_number
            )
            .join(PassTraveller, UserSensitiveInformation.user_id == PassTraveller.user_id)
            #.join(UserSensitiveInformation, UserSensitiveInformation.user_id == UserSensitiveInformation.user_id)
            .filter(PassTraveller.pass_id == p.pass_id)
            .all()
        )

        # Convert traveller data to JSON format
        travellers_list = [
            {
                "user_id": t.user_id,
                "first_name": t.first_name,
                "middle_name": t.middle_name,
                "last_name": t.last_name,
                "passport_number": t.passport_number
            }
            for t in travellers
        ]

        passes_list.append({
            "pass_id": p.pass_id,
            # "vehicle_id": p.vehicle_id,
            # "creation_datetime": p.creation_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "expiry_datetime": p.expiry_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "pass_date": p.pass_date.strftime("%Y-%m-%d %H:%M:%S"),
            # "origin_id": p.origin_id,
            # "destination_id": p.destination_id,
            "pass_utilized": p.pass_utilized,
            "travellers": travellers_list
        })

    return jsonify({
        "user_id": user_id,
        "passes": passes_list
    }), 200

@app.route('/api/passes/create', methods=['POST'])
def create_pass():

    # Extract data from request body
    data = request.get_json()

    vehicle_number = data.get("vehicle_number")
    creator_user_id = data.get("creator_user_id")
    pass_date = data.get("pass_date")
    pass_utilized = data.get("pass_utilized", False)
    traveller_passport_numbers = data.get("traveller_passport_numbers", [])

    # Validate required fields
    if not all([vehicle_number, creator_user_id, pass_date]):
        return jsonify({"error": "Missing required fields - Vehicle number, Pass user id and pass date"}), 400

    # Convert datetime strings to proper formats
    try:
        # creation_datetime = datetime.strptime(creation_datetime, "%Y-%m-%d %H:%M:%S")
        # expiry_datetime = datetime.strptime(expiry_datetime, "%Y-%m-%d %H:%M:%S")
        pass_date = datetime.strptime(pass_date, "%Y-%m-%d %H:%M:%S").date()
        expiry_datetime = pass_date + timedelta(hours=24) # Add 24 hours
    
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    # Check if the vehicle exists
    vehicle = Vehicle.query.filter_by(vehicle_number=vehicle_number).first()
    if not vehicle:
        return jsonify({"error": f"Vehicle with number {vehicle_number} not found"}), 404

    # Create new pass
    new_pass = Pass(
        # vehicle_id=vehicle_id,
        creator_user_id=creator_user_id,
        # creation_datetime=creation_datetime,
        expiry_datetime=expiry_datetime,
        pass_date=pass_date,
        pass_utilized=pass_utilized,
        # origin_id = 1,  # Default (1): Singapore
        # destination_id = 2  # Default (2): Johor Bahru
    )

    db.session.add(new_pass)
    db.session.commit()  # Commit to generate pass_id

    pass_id = new_pass.pass_id

    # List to store successfully added travellers
    travellers_added = []

    # Process each traveller
    for passport_number in traveller_passport_numbers:
        # Find user_id from passport_number
        user_sensitive = UserSensitiveInformation.query.filter_by(passport_number=passport_number).first()
        if not user_sensitive:
            return jsonify({"error": f"Traveller with passport number {passport_number} not found"}), 404

        traveller_user_id = user_sensitive.user_id

        # Add traveller to PassTravellers table
        pass_traveller = PassTraveller(pass_id=pass_id, user_id=traveller_user_id)
        db.session.add(pass_traveller)

        # Append to response list
        travellers_added.append({
            "user_id": traveller_user_id,
            "first_name": user_sensitive.first_name,
            "middle_name": user_sensitive.middle_name,
            "last_name": user_sensitive.last_name,
            "passport_number": passport_number
        })

    db.session.commit()  # Commit all travellers

    return jsonify({
        "message": "Pass created successfully",
        "pass_id": pass_id,
        # "vehicle_id": vehicle_id,
        "creator_user_id": creator_user_id,
        # "creation_datetime": creation_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        "expiry_datetime": expiry_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        "pass_date": pass_date.strftime("%Y-%m-%d %H:%M:%S"),
        "pass_utilized": pass_utilized,
        "travellers_added": travellers_added
    }), 201

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # return redirect(url_for('static', filename='uploads/' + filename), code=301)

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/api/users/<int:user_id>/passes/history', methods=['GET'])
def get_utilized_passes(user_id):

    # Check if the user exists
    user = UserSensitiveInformation.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Fetch all utilized passes created by the user
    utilized_passes = (
        db.session.query(
            Pass.pass_id,
            # Pass.vehicle_id,
            Pass.expiry_datetime,
            Pass.pass_date,
            #Pass.origin_id,
            # Pass.destination_id
        )
        .filter(Pass.creator_user_id == user_id, Pass.pass_utilized == True)
        .all()
    )

    # Convert results into JSON format
    passes_list = [
        {
            "pass_id": p.pass_id,
            # "vehicle_id": p.vehicle_id,
            # "creation_datetime": p.creation_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "expiry_datetime": p.expiry_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "pass_date": p.pass_date.strftime("%Y-%m-%d %H:%M:%S"),
            #"origin_id": p.origin_id,
            # "destination_id": p.destination_id
        }
        for p in utilized_passes
    ]

    return jsonify({
        "user_id": user_id,
        "passes_utilized": passes_list
    }), 200

# Updating first name of the user in the profile page
@app.route('/api/users/<int:user_id>/first-name', methods=['GET', 'POST'])
def manage_user_first_name(user_id):
    user = UserSensitiveInformation.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if request.method == 'GET':
        return jsonify({"first_name": user.first_name}), 200

    if request.method == 'POST':
        data = request.get_json()
        user.first_name = data.get("first_name", user.first_name)
        db.session.commit()
        return jsonify({"message": "First name updated successfully"}), 200


# Updating middle name of the user in the profile page
@app.route('/api/users/<int:user_id>/middle-name', methods=['GET', 'POST'])
def manage_user_middle_name(user_id):
    user = UserSensitiveInformation.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if request.method == 'GET':
        return jsonify({"middle_name": user.middle_name}), 200

    if request.method == 'POST':
        data = request.get_json()
        user.middle_name = data.get("middle_name", user.middle_name)
        db.session.commit()
        return jsonify({"message": "Middle name updated successfully"}), 200


# Updating last name of the user in the profile page
@app.route('/api/users/<int:user_id>/last-name', methods=['GET', 'POST'])
def manage_user_last_name(user_id):
    user = UserSensitiveInformation.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if request.method == 'GET':
        return jsonify({"last_name": user.last_name}), 200

    if request.method == 'POST':
        data = request.get_json()
        user.last_name = data.get("last_name", user.last_name)
        db.session.commit()
        return jsonify({"message": "Last name updated successfully"}), 200

# Updating Date of birth of the user in the profile page
@app.route('/api/users/<int:user_id>/dob', methods=['GET', 'POST'])
def manage_user_dob(user_id):
    user = UserSensitiveInformation.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if request.method == 'GET':
        return jsonify({"date_of_birth": user.date_of_birth.strftime("%Y-%m-%d")}), 200

    if request.method == 'POST':
        data = request.get_json()
        try:
            user.date_of_birth = datetime.strptime(data.get("date_of_birth"), "%Y-%m-%d").date()
            db.session.commit()
            return jsonify({"message": "Date of Birth updated successfully"}), 200
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400


# Updating Nationality aka Passport Issuing Country of the user in the profile page 
@app.route('/api/users/<int:user_id>/nationality', methods=['GET', 'POST'])
def manage_user_nationality(user_id):
    user = UserSensitiveInformation.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if request.method == 'GET':
        return jsonify({"nationality": user.passport_issuing_country}), 200

    if request.method == 'POST':
        data = request.get_json()
        user.passport_issuing_country = data.get("nationality", user.passport_issuing_country)
        db.session.commit()
        return jsonify({"message": "Nationality updated successfully"}), 200


# Updating Passport expiry of the user in the profile page 
@app.route('/api/users/<int:user_id>/passport-expiry', methods=['GET', 'POST'])
def manage_passport_expiry(user_id):
    user = UserSensitiveInformation.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if request.method == 'GET':
        return jsonify({"passport_expiry": user.passport_expiry.strftime("%Y-%m-%d")}), 200

    if request.method == 'POST':
        data = request.get_json()
        try:
            user.passport_expiry = datetime.strptime(data.get("passport_expiry"), "%Y-%m-%d")
            db.session.commit()
            return jsonify({"message": "Passport expiry date updated successfully"}), 200
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400


# Updating Passport number of the user in the profile page 
@app.route('/api/users/<int:user_id>/passport-number', methods=['GET', 'POST'])
def manage_passport_number(user_id):
    user = UserSensitiveInformation.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if request.method == 'GET':
        return jsonify({"passport_number": user.passport_number}), 200

    if request.method == 'POST':
        data = request.get_json()
        user.passport_number = data.get("passport_number", user.passport_number)
        db.session.commit()
        return jsonify({"message": "Passport number updated successfully"}), 200

# Retrieving all information of user in the profile page
@app.route('/api/users/<int:user_id>/profile', methods=['GET'])
def get_user_profile(user_id):
    user = UserSensitiveInformation.query.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Only middle name should be the truly optional field. Adding if-else statements for the rest to safely return None in JSON.
    profile_data = {
        "first_name": user.first_name if user.first_name else None,
        "middle_name": user.middle_name if user.middle_name else None,
        "last_name": user.last_name if user.last_name else None,
        "date_of_birth": user.date_of_birth.strftime("%Y-%m-%d") if user.date_of_birth else None,
        "nationality": user.passport_issuing_country if user.passport_issuing_country else None,
        "passport_expiry": user.passport_expiry.strftime("%Y-%m-%d") if user.passport_expiry else None,
        "passport_number": user.passport_number if user.passport_number else None
    }

    return jsonify(profile_data), 200

# Get all travellers (that are not associated with pass/preset) for a user
@app.route('/api/users/<int:user_id>/travellers', methods=['GET'])
def get_user_travellers(user_id):
    # Check if the creator user exists
    creator = UserSensitiveInformation.query.get(user_id)
    if not creator:
        return jsonify({"error": "User not found"}), 404

    # Query all travellers added by the creator
    travellers = (
        db.session.query(
            UserSensitiveInformation.user_id,
            UserSensitiveInformation.first_name,
            UserSensitiveInformation.middle_name,
            UserSensitiveInformation.last_name,
            UserSensitiveInformation.passport_number
        )
        .join(UserTraveller, UserSensitiveInformation.user_id == UserTraveller.traveller_id)
        .filter(UserTraveller.creator_user_id == user_id)
        .all()
    )

    # Convert traveller data to JSON format
    traveller_list = [
        {
            "traveller_id": t.user_id,
            "first_name": t.first_name,
            "middle_name": t.middle_name,
            "last_name": t.last_name,
            "passport_number": t.passport_number
        }
        for t in travellers
    ]

    return jsonify({
        "creator_user_id": user_id,
        "travellers": traveller_list
    }), 200

# Add a traveller (that is not associated with pass/preset) for a user
@app.route('/api/users/<int:user_id>/travellers', methods=['POST'])
def add_traveller(user_id):
    # Check if the creator user exists
    creator = UserSensitiveInformation.query.get(user_id)
    if not creator:
        return jsonify({"error": "Creator user not found"}), 404

    # Get JSON data
    data = request.get_json()
    passport_number = data.get("passport_number")

    if not passport_number:
        return jsonify({"error": "Passport number is required"}), 400

    # Find the traveller by passport number
    traveller = UserSensitiveInformation.query.filter_by(passport_number=passport_number).first()
    
    if not traveller:
        return jsonify({"error": "Traveller with this passport number not found"}), 404

    traveller_id = traveller.user_id

    # Check if traveller is already added by this user
    existing_entry = UserTraveller.query.filter_by(creator_user_id=user_id, traveller_id=traveller_id).first()
    if existing_entry:
        return jsonify({"error": "Traveller already added"}), 400

    # Add to UserTraveller table
    new_traveller = UserTraveller(creator_user_id=user_id, traveller_id=traveller_id)
    db.session.add(new_traveller)
    db.session.commit()

    return jsonify({
        "message": "Traveller added successfully",
        "creator_user_id": user_id,
        "traveller": {
            "traveller_id": traveller.user_id,
            "first_name": traveller.first_name,
            "middle_name": traveller.middle_name,
            "last_name": traveller.last_name,
            "passport_number": traveller.passport_number
        }
    }), 201

if __name__ == '__main__':

    with app.app_context():

        # Drop all tables to start fresh
        db.drop_all()

        # Create database tables
        db.create_all() 

        # Insert mock data
        insert_mock_data()  

    app.run(debug=True, host='0.0.0.0', port=5000)
