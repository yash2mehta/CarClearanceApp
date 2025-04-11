from flask_restx import Namespace, Resource
from flask import request
from app.services.vehicle_service import VehicleService
from app.api.schemas import (
    add_vehicle_model, all_vehicles_model,
    error_response_model_400, error_response_model_404,
    success_message_model
)

ns_vehicle = Namespace('vehicles', description='Vehicle-related operations')

@ns_vehicle.route('/<int:user_id>/add-vehicle')
class UserVehicleResource(Resource):
    """Add a vehicle to a user."""

    @ns_vehicle.expect(add_vehicle_model)
    @ns_vehicle.response(200, 'Vehicle added successfully', add_vehicle_model)
    @ns_vehicle.response(400, 'Missing vehicle number or user vehicle model', error_response_model_400)
    @ns_vehicle.response(404, 'User not found', error_response_model_404)
    def post(self, user_id):
        """Add a vehicle to the user"""
        data = request.get_json()
        vehicle_number = data.get('vehicle_number')
        user_vehicle_model = data.get('user_vehicle_model')

        if not vehicle_number:
            return {"error_code": 400, "message": "Missing vehicle_number"}, 400
        if not user_vehicle_model:
            return {"error_code": 400, "message": "Missing user_vehicle_model"}, 400

        result, error = VehicleService.add_vehicle(user_id, vehicle_number, user_vehicle_model)
        if error:
            if error == "User not found":
                return {"error_code": 404, "message": error}, 404
            return {"error_code": 400, "message": error}, 400

        return result, 200

@ns_vehicle.route('/<int:user_id>/get-all-vehicles')
class UserVehiclesResource(Resource):
    """Get all vehicles associated with a user."""

    @ns_vehicle.response(200, 'Success', all_vehicles_model)
    @ns_vehicle.response(404, 'User not found', error_response_model_404)
    def get(self, user_id):
        """Retrieve all vehicles linked to a user."""
        vehicles, error = VehicleService.get_user_vehicles(user_id)
        if error:
            return {"error_code": 404, "message": error}, 404
        return vehicles, 200

@ns_vehicle.route('/<int:user_id>/delete-vehicle-by-number')
class DeleteVehicleResource(Resource):
    """Delete a vehicle from a user's vehicle list based on vehicle number"""

    @ns_vehicle.expect(add_vehicle_model)
    @ns_vehicle.response(200, 'Vehicle deleted successfully', success_message_model)
    @ns_vehicle.response(400, 'Required fields missing', error_response_model_400)
    @ns_vehicle.response(404, 'User, vehicle or association not found', error_response_model_404)
    def delete(self, user_id):
        """Delete a vehicle from the user's list of vehicles by vehicle number."""
        data = request.get_json()
        vehicle_number = data.get("vehicle_number")

        if not vehicle_number:
            return {"error_code": 400, "message": "Vehicle number is required"}, 400

        result, error = VehicleService.delete_vehicle_by_number(user_id, vehicle_number)
        if error:
            if error == "User not found":
                return {"error_code": 404, "message": error}, 404
            return {"error_code": 400, "message": error}, 400

        return result, 200 