from flask_restx import Resource
from flask import request
from db_instance import db
from models import UserSensitiveInformation, Vehicle, UserVehicle
from api_models import (
    add_vehicle_model,
    add_vehicle_model_result,
    all_vehicles_model,
    error_response_model_400,
    error_response_model_404,
    delete_vehicle_model,
    delete_message_model
)
from .api_logger import log_api_access

def init_vehicle_routes(api):
    ns_vehicle = api.namespace('vehicles', description='Vehicle-related operations')
    
    @ns_vehicle.route('/<int:user_id>/add-vehicle')
    class UserVehicleResource(Resource):
        """Add a vehicle to a user."""
        @api.expect(add_vehicle_model)
        @api.response(200, 'Vehicle added successfully', add_vehicle_model_result)
        @api.response(400, 'Missing vehicle number or user vehicle model', error_response_model_400)
        @api.response(404, 'User or vehicle not found', error_response_model_404)
        @log_api_access('POST /vehicles/<user_id>/add-vehicle')
        def post(self, user_id):
            """Add a vehicle to the user"""
            user = UserSensitiveInformation.query.get(user_id)
            if not user:
                return {"error_code": 404, "message": "User not found"}, 404

            data = request.get_json()
            vehicle_number = data.get('vehicle_number')
            user_vehicle_model = data.get('user_vehicle_model') 

            if not vehicle_number:
                return {"error_code": 400, "message": "Missing vehicle_number"}, 400
            if not user_vehicle_model:
                return {"error_code": 400, "message": "Missing user_vehicle_model"}, 400

            vehicle = Vehicle.query.filter_by(vehicle_number=vehicle_number).first()
            if not vehicle:
                vehicle = Vehicle(vehicle_number=vehicle_number)
                db.session.add(vehicle)
                db.session.commit()

            user_vehicle = UserVehicle(
                user_id=user_id,
                vehicle_id=vehicle.vehicle_id,
                user_vehicle_model=user_vehicle_model
            )

            db.session.add(user_vehicle)
            db.session.commit()
            
            response = {
                "user_vehicle": {
                    "user_id": user_id,
                    "vehicle_id": vehicle.vehicle_id,
                    "vehicle_number": vehicle.vehicle_number,
                    "user_vehicle_model": user_vehicle_model
                }
            }
            return api.marshal(response, add_vehicle_model_result), 200


    @ns_vehicle.route('/<int:user_id>/delete-vehicle-by-number')
    class DeleteVehicleResource(Resource):
        """Delete a vehicle from a user's vehicle list based on vehicle number"""

        @api.expect(delete_vehicle_model)
        @api.response(200, 'Vehicle deleted successfully', delete_message_model)
        @api.response(400, 'Required fields missing', error_response_model_400)
        @api.response(404, 'User, vehicle or association not found', error_response_model_404)
        @log_api_access('DELETE /vehicles/<user_id>/delete-vehicle-by-number')
        def delete(self, user_id):
            """Delete a vehicle from the user's list of vehicles by vehicle number."""
            user = UserSensitiveInformation.query.get(user_id)
            if not user:
                return {"error_code": 404, "message": "User not found"}, 404
            data = request.get_json()
            vehicle_number = data.get("vehicle_number")

            if not vehicle_number:
                return {"error_code": 400, "message": "Vehicle number is required"}, 400
            vehicle = Vehicle.query.filter_by(vehicle_number=vehicle_number).first()
            if not vehicle:
                return {"error_code": 404, "message": "Vehicle with this number not found"}, 404

            vehicle_id = vehicle.vehicle_id
            user_vehicle = UserVehicle.query.filter_by(
                user_id=user_id,
                vehicle_id=vehicle_id
            ).first()

            if not user_vehicle:
                return {
                    "error_code": 404, 
                    "message": "This vehicle is not in your vehicle list"
                }, 404
            db.session.delete(user_vehicle)
            db.session.commit()

            return {"message": f"Vehicle with number {vehicle_number} removed from your vehicles list"}, 200


    @ns_vehicle.route('/<int:user_id>/get-all-vehicles')
    class UserVehiclesResource(Resource):
        """Get all vehicles associated with a user."""
        @api.response(200, 'Success', all_vehicles_model) 
        @api.response(404, 'User not found', error_response_model_404)
        @log_api_access('GET /vehicles/<user_id>/get-all-vehicles')
        def get(self, user_id):
            """Retrieve all vehicles linked to a user."""
            user = UserSensitiveInformation.query.get(user_id)
            if not user:
                return {"error_code": 404, "message": "User not found"}, 404
            
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

            return api.marshal(vehicles_list, all_vehicles_model), 200

    return ns_vehicle 