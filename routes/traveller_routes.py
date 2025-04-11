from flask_restx import Resource
from flask import request
from db_instance import db
from models import UserSensitiveInformation, UserTraveller
from api_models import (
    error_response_model_400,
    error_response_model_404,
    success_message_model,
    user_travellers_model,
    batch_add_travellers_model,
    batch_add_travellers_response_model,
    passport_number_model,
    delete_traveller_by_passport_model
)
from .api_logger import log_api_access

def init_traveller_routes(api):
    ns_traveller = api.namespace('travellers', description='Traveller management')

    @ns_traveller.route('/<int:user_id>/get-travellers')
    class UserTravellersResource(Resource):
        """Get all travellers (that are not associated with pass/preset) for a user."""
        @api.response(200, 'Travellers retrieved successfully', user_travellers_model)
        @api.response(404, 'User not found', error_response_model_404)
        @api.response(400, 'Bad request due to incorrect data', error_response_model_400)
        @log_api_access('GET /travellers/<user_id>/get-travellers')
        def get(self, user_id):
            """Retrieve all travellers added by the user that are not associated with a pass or preset."""
            creator = UserSensitiveInformation.query.get(user_id)
            if not creator:
                return {"error_code": 404, "message": "User not found"}, 404
            
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
            
            traveller_list = [
                {
                    "user_id": t.user_id,
                    "first_name": t.first_name,
                    "middle_name": t.middle_name,
                    "last_name": t.last_name,
                    "passport_number": t.passport_number
                }
                for t in travellers
            ]
            
            response = {
                "creator_user_id": user_id,
                "travellers": traveller_list
            }
            return api.marshal(response, user_travellers_model), 200

    @ns_traveller.route('/<int:user_id>/add-traveller')
    class AddTravellerResource(Resource):
        """Add a traveller (not associated with pass/preset) for a user."""
        @api.expect(passport_number_model)
        @api.response(201, 'Traveller added successfully', user_travellers_model)
        @api.response(400, 'Required fields missing or data already in database', error_response_model_400)
        @api.response(404, 'Resource not found', error_response_model_404)
        @log_api_access('POST /travellers/<user_id>/add-traveller')
        def post(self, user_id):    
            """Add a traveller for the user."""
            creator = UserSensitiveInformation.query.get(user_id)
            if not creator:
                return {"error_code": 404, "message": "Creator user not found"}, 404
            
            data = request.get_json()
            passport_number = data.get("passport_number")

            if not passport_number:
                return {"error_code": 400, "message": "Passport number is required"}, 400
            
            traveller = UserSensitiveInformation.query.filter_by(passport_number=passport_number).first()
            
            if not traveller:
                return {"error_code": 404, "message": "Traveller with this passport number not found"}, 404

            traveller_id = traveller.user_id
            existing_entry = UserTraveller.query.filter_by(creator_user_id=user_id, traveller_id=traveller_id).first()
            if existing_entry:
                return {"error_code": 400, "message": "Traveller already added"}, 400
            
            new_traveller = UserTraveller(creator_user_id=user_id, traveller_id=traveller_id)
            db.session.add(new_traveller)
            db.session.commit()
            
            response = {
                "creator_user_id": user_id,
                "travellers": {
                    "user_id": traveller.user_id,
                    "first_name": traveller.first_name,
                    "middle_name": traveller.middle_name,
                    "last_name": traveller.last_name,
                    "passport_number": traveller.passport_number
                }
            }

            return api.marshal(response, user_travellers_model), 201


    @ns_traveller.route('/<int:user_id>/delete-traveller-by-passport')
    class DeleteTravellerByPassportResource(Resource):
        """Delete a traveller from a user's traveller list based on the traveller's passport number"""

        @api.expect(delete_traveller_by_passport_model)
        @api.response(200, 'Traveller deleted successfully', success_message_model)
        @api.response(400, 'Required fields missing', error_response_model_400)
        @api.response(404, 'User or traveller not found', error_response_model_404)
        @log_api_access('DELETE /travellers/<user_id>/delete-traveller-by-passport')
        def delete(self, user_id):
            """Delete a traveller from the user's list of travellers by passport number."""
            creator_user = UserSensitiveInformation.query.get(user_id)
            if not creator_user:
                return {"error_code": 404, "message": "Creator user not found"}, 404
            data = request.get_json()
            passport_number = data.get("passport_number")

            if not passport_number:
                return {"error_code": 400, "message": "Passport number is required"}, 400
            traveller = UserSensitiveInformation.query.filter_by(passport_number=passport_number).first()
            if not traveller:
                return {"error_code": 404, "message": "Traveller with this passport number not found"}, 404

            traveller_id = traveller.user_id
            user_traveller = UserTraveller.query.filter_by(
                creator_user_id=user_id,
                traveller_id=traveller_id
            ).first()

            if not user_traveller:
                return {
                    "error_code": 404, 
                    "message": "This traveller is not in your traveller list"
                }, 404
            db.session.delete(user_traveller)
            db.session.commit()

            return {"message": f"Traveller with passport number {passport_number} deleted successfully"}, 200

    @ns_traveller.route('/batch-add-travellers')
    class BatchAddTravellersResource(Resource):
        """Check if travellers exist in a user's list and add them if not."""

        @api.expect(batch_add_travellers_model)
        @api.response(200, 'Travellers processed successfully', batch_add_travellers_response_model)
        @api.response(400, 'Required fields missing', error_response_model_400)
        @api.response(404, 'User or traveller not found', error_response_model_404)
        @log_api_access('POST /travellers/batch-add-travellers')
        def post(self):
            """Check if travellers with given passport numbers are in a user's list and add them if not."""
            data = request.get_json()
            user_id = data.get("user_id")
            passport_numbers = data.get("passport_numbers", [])
            if not user_id:
                return {"error_code": 400, "message": "User ID is required"}, 400
            
            if not isinstance(passport_numbers, list) or not passport_numbers:
                return {"error_code": 400, "message": "Passport numbers list is required and cannot be empty"}, 400
            creator = UserSensitiveInformation.query.get(user_id)
            if not creator:
                return {"error_code": 404, "message": "User not found"}, 404
            existing_traveller_ids = db.session.query(UserTraveller.traveller_id)\
                .filter(UserTraveller.creator_user_id == user_id)\
                .all()
            existing_traveller_ids = [t[0] for t in existing_traveller_ids]
            
            travellers_added = []
            travellers_already_present = []
            
            try:
                for passport_number in passport_numbers:
                    traveller = UserSensitiveInformation.query.filter_by(passport_number=passport_number).first()
                    
                    if not traveller:
                        return {"error_code": 404, "message": f"Traveller with passport number {passport_number} not found"}, 404
                    if traveller.user_id in existing_traveller_ids:
                        travellers_already_present.append({
                            "user_id": traveller.user_id,
                            "first_name": traveller.first_name,
                            "middle_name": traveller.middle_name,
                            "last_name": traveller.last_name,
                            "passport_number": traveller.passport_number
                        })
                    else:
                        new_traveller = UserTraveller(creator_user_id=user_id, traveller_id=traveller.user_id)
                        db.session.add(new_traveller)
                        
                        travellers_added.append({
                            "user_id": traveller.user_id,
                            "first_name": traveller.first_name,
                            "middle_name": traveller.middle_name,
                            "last_name": traveller.last_name,
                            "passport_number": traveller.passport_number
                        })
                db.session.commit()
                response = {
                    "user_id": user_id,
                    "travellers_added": travellers_added,
                    "travellers_already_present": travellers_already_present
                }
                
                return api.marshal(response, batch_add_travellers_response_model), 200
                
            except Exception as e:
                db.session.rollback()
                return {"error_code": 400, "message": f"Error processing travellers: {str(e)}"}, 400

    return ns_traveller 

