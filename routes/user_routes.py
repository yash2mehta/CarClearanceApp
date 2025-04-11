from flask_restx import Resource
from flask import request
from db_instance import db
from models import UserSensitiveInformation
from api_models import (
    user_profile_model,
    user_profile_with_id_model,
    error_response_model_400,
    error_response_model_404,
    success_message_model,
    name_by_passport_request_model,
    name_by_passport_response_model,
    traveller_model
)

def init_user_routes(api):
    ns_user = api.namespace('users', description='User-related operations')

    @ns_user.route('/retrieve-name-by-passport')
    class RetrieveNameByPassportResource(Resource):
        """Retrieve name information based on passport number."""

        @api.expect(name_by_passport_request_model)
        @api.response(200, 'Success', name_by_passport_response_model)
        @api.response(400, 'Missing passport number', error_response_model_400)
        @api.response(404, 'User or passport not found', error_response_model_404)
        def post(self):
            """Retrieve first name, middle name, last name and full name by passport number."""
            data = request.get_json()
            passport_number = data.get("passport_number")

            if not passport_number:
                return {"error_code": 400, "message": "Passport number is required"}, 400
            person = UserSensitiveInformation.query.filter_by(passport_number=passport_number).first()
            if not person:
                return {"error_code": 404, "message": "Person with this passport number not found"}, 404
            name_parts = []
            if person.first_name:
                name_parts.append(person.first_name)
            if person.middle_name:
                name_parts.append(person.middle_name)
            if person.last_name:
                name_parts.append(person.last_name)
            
            full_name = " ".join(name_parts)
            response = {
                "first_name": person.first_name,
                "middle_name": person.middle_name,
                "last_name": person.last_name,
                "full_name": full_name
            }

            return api.marshal(response, name_by_passport_response_model), 200


    @ns_user.route('/<int:user_id>/profile')
    class UserProfileResource(Resource):
        """Retrieve the profile of the user."""
        @api.response(200, 'User profile retrieved successfully', user_profile_model)
        @api.response(404, 'User not found', error_response_model_404)
        def get(self, user_id):
            """Get all the information of the user."""
            user = UserSensitiveInformation.query.get(user_id)

            if not user:
                return {"error_code": 404, "message": "User not found"}, 404
            
            profile_data = {
                "first_name": user.first_name if user.first_name else None,
                "middle_name": user.middle_name if user.middle_name else None,
                "last_name": user.last_name if user.last_name else None,
                "date_of_birth": user.date_of_birth.strftime("%Y-%m-%d") if user.date_of_birth else None,
                "nationality": user.passport_issuing_country if user.passport_issuing_country else None,
                "passport_expiry": user.passport_expiry.strftime("%Y-%m-%d") if user.passport_expiry else None,
                "passport_number": user.passport_number if user.passport_number else None
            }

            return api.marshal(profile_data, user_profile_model), 200


    @ns_user.route('/<int:user_id>/update-traveller')
    @api.param('user_id', 'The user identifier')
    class UpdateTravellerResource(Resource):
        @api.expect(traveller_model)
        @api.response(200, 'Traveller updated successfully', traveller_model)
        @api.response(400, 'Invalid data format', error_response_model_400)
        @api.response(404, 'User ID not found', error_response_model_404)
        def put(self, user_id):
            data = request.get_json()

            user = UserSensitiveInformation.query.get(user_id)
            if not user:
                return {"error_code": 404, "message": "User not found"}, 404

            try:
                traveller = Traveller.query.filter_by(user_id=user_id).first()
                if not traveller:
                    return {"error_code": 404, "message": "Traveller not found"}, 404

                if 'passport_number' in data and data['passport_number']:
                    traveller.passport_number = data['passport_number']

                if 'first_name' in data and data['first_name']:
                    traveller.first_name = data['first_name']

                if 'middle_name' in data and data['middle_name']:
                    traveller.middle_name = data['middle_name']

                if 'last_name' in data and data['last_name']:
                    traveller.last_name = data['last_name']

                if 'date_of_birth' in data and data['date_of_birth']:
                    try:
                        traveller.date_of_birth = datetime.strptime(data['date_of_birth'], "%Y-%m-%d").date()
                    except ValueError:
                        return {"error_code": 400, "message": "Invalid date format for date_of_birth. Use YYYY-MM-DD"}, 400

                if 'nationality' in data and data['nationality']:
                    traveller.nationality = data['nationality']

                db.session.commit()

                response_data = {
                    "passport_number": traveller.passport_number,
                    "first_name": traveller.first_name,
                    "middle_name": traveller.middle_name,
                    "last_name": traveller.last_name,
                    "date_of_birth": traveller.date_of_birth.strftime("%Y-%m-%d") if traveller.date_of_birth else None,
                    "nationality": traveller.nationality
                }

                return api.marshal(response_data, traveller_model), 200

            except Exception as e:
                db.session.rollback()
                return {"error_code": 400, "message": f"Error updating traveller: {str(e)}"}, 400


    @ns_user.route('/<int:user_id>/update-profile')
    class UpdateUserProfileResource(Resource):
        @api.expect(user_profile_model)
        @api.response(200, 'User profile updated successfully', user_profile_with_id_model)
        @api.response(400, 'Invalid data format', error_response_model_400)
        @api.response(404, 'User ID not found', error_response_model_404)
        def put(self, user_id):
            data = request.get_json()

            user = UserSensitiveInformation.query.get(user_id)
            if not user:
                return {"error_code": 404, "message": "User not found"}, 404

            try:
                if 'first_name' in data and data['first_name']:
                    user.first_name = data['first_name']

                if 'middle_name' in data and data['middle_name']:
                    user.middle_name = data['middle_name']

                if 'last_name' in data and data['last_name']:
                    user.last_name = data['last_name']

                if 'date_of_birth' in data and data['date_of_birth']:
                    try:
                        user.date_of_birth = datetime.strptime(data['date_of_birth'], "%Y-%m-%d").date()
                    except ValueError:
                        return {"error_code": 400, "message": "Invalid date format for date_of_birth. Use YYYY-MM-DD"}, 400

                if 'nationality' in data and data['nationality']:
                    user.passport_issuing_country = data['nationality']

                if 'passport_expiry' in data and data['passport_expiry']:
                    try:
                        user.passport_expiry = datetime.strptime(data['passport_expiry'], "%Y-%m-%d")
                    except ValueError:
                        return {"error_code": 400, "message": "Invalid date format for passport_expiry. Use YYYY-MM-DD"}, 400

                if 'passport_number' in data and data['passport_number']:
                    user.passport_number = data['passport_number']

                db.session.commit()

                response_data = {
                    "user_id": user_id,
                    "first_name": user.first_name,
                    "middle_name": user.middle_name,
                    "last_name": user.last_name,
                    "date_of_birth": user.date_of_birth.strftime("%Y-%m-%d") if user.date_of_birth else None,
                    "nationality": user.passport_issuing_country,
                    "passport_expiry": user.passport_expiry.strftime("%Y-%m-%d") if user.passport_expiry else None,
                    "passport_number": user.passport_number
                }

                return api.marshal(response_data, user_profile_with_id_model), 200

            except Exception as e:
                db.session.rollback()
                return {"error_code": 400, "message": f"Error updating user profile: {str(e)}"}, 400

    return ns_user 

    