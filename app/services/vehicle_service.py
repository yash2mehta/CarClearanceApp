from app import db
from app.api.models import Vehicle, UserVehicle, UserSensitiveInformation
from app.utils.validators import validate_vehicle_number

class VehicleService:
    @staticmethod
    def add_vehicle(user_id, vehicle_number, user_vehicle_model):
        """Add a vehicle to a user's list."""
        if not validate_vehicle_number(vehicle_number):
            return None, "Invalid vehicle number format"

        user = UserSensitiveInformation.query.get(user_id)
        if not user:
            return None, "User not found"

        # Check if vehicle exists, if not create it
        vehicle = Vehicle.query.filter_by(vehicle_number=vehicle_number).first()
        if not vehicle:
            vehicle = Vehicle(vehicle_number=vehicle_number)
            db.session.add(vehicle)
            db.session.commit()

        # Check if user already has this vehicle
        existing_user_vehicle = UserVehicle.query.filter_by(
            user_id=user_id,
            vehicle_id=vehicle.vehicle_id
        ).first()

        if existing_user_vehicle:
            return None, "Vehicle already added to user's list"

        # Create user-vehicle association
        user_vehicle = UserVehicle(
            user_id=user_id,
            vehicle_id=vehicle.vehicle_id,
            user_vehicle_model=user_vehicle_model
        )
        db.session.add(user_vehicle)
        db.session.commit()

        return {
            "user_vehicle": {
                "user_id": user_id,
                "vehicle_id": vehicle.vehicle_id,
                "vehicle_number": vehicle.vehicle_number,
                "user_vehicle_model": user_vehicle_model
            }
        }, None

    @staticmethod
    def get_user_vehicles(user_id):
        """Get all vehicles associated with a user."""
        user = UserSensitiveInformation.query.get(user_id)
        if not user:
            return None, "User not found"

        user_vehicles = (
            db.session.query(UserVehicle, Vehicle)
            .join(Vehicle, UserVehicle.vehicle_id == Vehicle.vehicle_id)
            .filter(UserVehicle.user_id == user_id)
            .all()
        )

        vehicles_list = []
        for uv, v in user_vehicles:
            vehicles_list.append({
                'user_vehicle_id': uv.user_vehicle_id,
                'user_vehicle_name': uv.user_vehicle_model,
                'vehicle_id': v.vehicle_id,
                'vehicle_number': v.vehicle_number
            })

        return vehicles_list, None

    @staticmethod
    def delete_vehicle_by_number(user_id, vehicle_number):
        """Delete a vehicle from user's list by vehicle number."""
        user = UserSensitiveInformation.query.get(user_id)
        if not user:
            return None, "User not found"

        vehicle = Vehicle.query.filter_by(vehicle_number=vehicle_number).first()
        if not vehicle:
            return None, "Vehicle not found"

        user_vehicle = UserVehicle.query.filter_by(
            user_id=user_id,
            vehicle_id=vehicle.vehicle_id
        ).first()

        if not user_vehicle:
            return None, "Vehicle not in user's list"

        db.session.delete(user_vehicle)
        db.session.commit()

        return {"message": f"Vehicle with number {vehicle_number} removed from your vehicles list"}, None 