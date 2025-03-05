from datetime import datetime, timezone
from db_instance import db
from sqlalchemy import func
from models import Vehicle, Pass, UserVehicle, PassTraveller, User  # Import relevant models

# Immigration Checkpoint Workflow Logic
def immigration_walkthrough(license_plate):

    # Check if the vehicle exists in the database
    vehicle = Vehicle.query.filter(func.lower(Vehicle.vehicle_number) == license_plate.lower()).first()
    
    if not vehicle:
        return {"status": "failure", "message": "Vehicle not found in the system. Please register the vehicle."}

    # Get all users linked to the vehicle from UserVehicle table
    user_vehicles = UserVehicle.query.filter_by(vehicle_id=vehicle.vehicle_id).all()

    if not user_vehicles:
        return {"status": "failure", "message": "No users found linked to this vehicle."} 

    # Store a list of all user_ids - Those users have registered the vehicle
    user_ids = [uv.user_id for uv in user_vehicles]

    valid_pass = None
    
    for user_id in user_ids:

        # Retrieve the user's pass from the Pass table
        passes = Pass.query.filter_by(vehicle_id=vehicle.vehicle_id, creator_user_id=user_id).all()

        #TODO - Incorporate logic for querying next pass if current pass in invalid

        # Apply additional filtering to the passes - only select those passes 
        for p in passes:

            # Make expiry_datetime aware of UTC timezone if it doesn't already have one
            if p.expiry_datetime.tzinfo is None:
                expiry_datetime_aware = p.expiry_datetime.replace(tzinfo=timezone.utc)
            else:
                expiry_datetime_aware = p.expiry_datetime

            if expiry_datetime_aware > datetime.now(timezone.utc):
                valid_pass = p
                break
        
        if valid_pass:
            break

    if not valid_pass:
        return {"status": "failure", "message": "No valid pass found for today."}
    

    # Select those rows in PassTraveller which has valid pass id
    pass_travellers = PassTraveller.query.filter_by(pass_id=valid_pass.pass_id).all()

    # Get all the user ids of the travellers in the group for that particular valid pass
    traveller_ids = [pt.user_id for pt in pass_travellers]

    # Select those rows in User table if the User id falls under traveller_ids list
    travellers = User.query.filter(User.user_id.in_(traveller_ids)).all()

    # Get the first and last name for the travellers
    traveller_info = [{"first_name": trav.first_name, "last_name": trav.last_name} for trav in travellers]

    #TODO - Need to incorporate logic of communicating with kiosk here to check if the pass retrieved is valid

    # If a valid pass is found, provide a success message including traveller names
    return {"status": "success", "travellers": traveller_info}
