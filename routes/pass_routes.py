from flask_restx import Resource
from flask import request
from datetime import datetime, timedelta
from db_instance import db
from models import UserSensitiveInformation, Pass, PassTraveller
from api_models import (
    pass_response_model,
    pass_response_model_2,
    pass_details_by_id_model,
    pass_details_by_user_model,
    pass_details_request_model,
    pass_history_with_travellers_model,
    create_pass_model,
    delete_pass_model,
    update_pass_model,
    error_response_model_400,
    error_response_model_404,
    success_message_model
)
from .api_logger import log_api_access

def init_pass_routes(api):
    ns_pass = api.namespace('passes', description='Pass-related operations')

    @ns_pass.route('/<int:user_id>/passes')
    class UserPassesResource(Resource):
        @api.response(200, 'Success', pass_response_model)
        @api.response(404, 'User ID not found', error_response_model_404)
        @log_api_access('GET /passes/<user_id>/passes')
        def get(self, user_id):
            user = UserSensitiveInformation.query.get(user_id)
            if not user:
                return {"error": "User not found"}, 404

            passes = (
                db.session.query(
                    Pass.pass_id,
                    Pass.pass_date,
                    Pass.expiry_datetime,
                    Pass.pass_utilized
                )
                .filter(Pass.creator_user_id == user_id)
                .all()
            )

            passes_list = []
            for p in passes:
                travellers = (
                    db.session.query(
                        UserSensitiveInformation.user_id,
                        UserSensitiveInformation.first_name,
                        UserSensitiveInformation.middle_name,
                        UserSensitiveInformation.last_name,
                        UserSensitiveInformation.passport_number
                    )
                    .join(PassTraveller, UserSensitiveInformation.user_id == PassTraveller.user_id)
                    .filter(PassTraveller.pass_id == p.pass_id)
                    .all()
                )

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
                    "expiry_datetime": p.expiry_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    "pass_date": p.pass_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "pass_utilized": p.pass_utilized,
                    "travellers": travellers_list
                })

            response = {
                "user_id": user_id,
                "passes": passes_list
            }

            return api.marshal(response, pass_response_model), 200

    @ns_pass.route('/details')
    class PassDetailsByIdResource(Resource):
        """Get details for a specific pass ID."""
        @api.expect(pass_details_request_model)
        @api.response(200, 'Success', pass_details_by_id_model)
        @api.response(400, 'Missing pass ID', error_response_model_400)
        @api.response(404, 'Pass not found', error_response_model_404)
        @log_api_access('POST /passes/details')
        def post(self):
            """Retrieve details of a specific pass including pass date, expiry datetime, travellers, and passenger count."""
            data = request.get_json()
            pass_id = data.get("pass_id")
            if not pass_id:
                return {"error_code": 400, "message": "Pass ID is required"}, 400
            
            pass_entry = Pass.query.get(pass_id)
            if not pass_entry:
                return {"error_code": 404, "message": "Pass not found"}, 404
            
            travellers = (
                db.session.query(
                    UserSensitiveInformation.user_id,
                    UserSensitiveInformation.first_name,
                    UserSensitiveInformation.middle_name,
                    UserSensitiveInformation.last_name,
                    UserSensitiveInformation.passport_number
                )
                .join(PassTraveller, UserSensitiveInformation.user_id == PassTraveller.user_id)
                .filter(PassTraveller.pass_id == pass_id)
                .all()
            )
            
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
            
            passenger_count = len(travellers_list)
            response = {
                "pass_id": pass_id,
                "pass_date": pass_entry.pass_date.strftime("%Y-%m-%d %H:%M:%S"),
                "expiry_datetime": pass_entry.expiry_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "pass_utilized": pass_entry.pass_utilized,
                "passenger_count": passenger_count,
                "travellers": travellers_list
            }

            return api.marshal(response, pass_details_by_id_model), 200

    @ns_pass.route('/create')
    class CreatePassResource(Resource):
        @api.expect(create_pass_model)
        @api.response(200, 'Success', pass_response_model_2)
        @api.response(400, 'Missing required fields like Pass user id and pass date or invalid date format ', error_response_model_400)
        @api.response(404, 'Resource not found', error_response_model_404)
        @log_api_access('POST /passes/create')
        def post(self):
            data = request.get_json()

            creator_user_id = data.get("creator_user_id")
            pass_date = data.get("pass_date")
            pass_utilized = data.get("pass_utilized", False)
            traveller_passport_numbers = data.get("traveller_passport_numbers", [])

            if not all([creator_user_id, pass_date]):
                return {"error": "Missing required fields - Pass user id and pass date"}, 400

            try:
                pass_date = datetime.strptime(pass_date, "%Y-%m-%d %H:%M:%S").date()
                expiry_datetime = pass_date + timedelta(hours=24)
        
            except ValueError:
                return {"error": "Invalid date format"}, 400

            new_pass = Pass(
                creator_user_id=creator_user_id,
                expiry_datetime=expiry_datetime,
                pass_date=pass_date,
                pass_utilized=pass_utilized,
            )

            db.session.add(new_pass)
            db.session.commit()

            pass_id = new_pass.pass_id

            travellers_added = []

            for passport_number in traveller_passport_numbers:
                user_sensitive = UserSensitiveInformation.query.filter_by(passport_number=passport_number).first()
                if not user_sensitive:
                    return {"error": f"Traveller with passport number {passport_number} not found"}, 404

                traveller_user_id = user_sensitive.user_id

                pass_traveller = PassTraveller(pass_id=pass_id, user_id=traveller_user_id)
                db.session.add(pass_traveller)

                travellers_added.append({
                    "user_id": traveller_user_id,
                    "first_name": user_sensitive.first_name,
                    "middle_name": user_sensitive.middle_name,
                    "last_name": user_sensitive.last_name,
                    "passport_number": passport_number
                })

            db.session.commit()

            response = {
                "pass_id": pass_id,
                "creator_user_id": creator_user_id,
                "pass_date": pass_date.strftime("%Y-%m-%d %H:%M:%S"),
                "expiry_datetime": expiry_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "pass_utilized": pass_utilized,
                "travellers_added": travellers_added
            }

            return api.marshal(response, pass_response_model_2), 200

    @ns_pass.route('/<int:user_id>/passes-history-all')
    class UserPassHistoryWithTravellersResource(Resource):
        @api.response(200, 'Success', pass_history_with_travellers_model)
        @api.response(404, 'Resource not found', error_response_model_404)
        @log_api_access('GET /passes/<user_id>/passes-history-all')
        def get(self, user_id):
            user = UserSensitiveInformation.query.get(user_id)
            if not user:
                return {"error_code": 404, "message": "User not found"}, 404

            utilized_passes = (
                db.session.query(
                    Pass.pass_id,
                    Pass.pass_date,
                    Pass.expiry_datetime
                )
                .filter(Pass.creator_user_id == user_id, Pass.pass_utilized == True)
                .all()
            )

            passes_list = []
            for p in utilized_passes:
                travellers = (
                    db.session.query(
                        UserSensitiveInformation.user_id,
                        UserSensitiveInformation.first_name,
                        UserSensitiveInformation.middle_name,
                        UserSensitiveInformation.last_name,
                        UserSensitiveInformation.passport_number
                    )
                        .join(PassTraveller, UserSensitiveInformation.user_id == PassTraveller.user_id)
                        .filter(PassTraveller.pass_id == p.pass_id)
                    .all()
                )
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
                    "pass_date": p.pass_date,
                    "expiry_datetime": p.expiry_datetime,
                    "travellers": travellers_list
                })

                response = {
                "user_id": user_id,
                "passes_utilized": passes_list
            }
            return api.marshal(response, pass_history_with_travellers_model), 200

    @ns_pass.route('/<int:user_id>/delete-pass')
    class DeletePassResource(Resource):
        @api.expect(delete_pass_model)
        @api.response(200, 'Pass deleted successfully', success_message_model)
        @api.response(400, 'Required fields missing', error_response_model_400)
        @api.response(404, 'User, pass not found, or pass does not belong to user', error_response_model_404)
        @log_api_access('DELETE /passes/<user_id>/delete-pass')
        def delete(self, user_id):
            user = UserSensitiveInformation.query.get(user_id)
            if not user:
                return {"error_code": 404, "message": "User not found"}, 404

            data = request.get_json()
            pass_id = data.get("pass_id")

            if not pass_id:
                return {"error_code": 400, "message": "Pass ID is required"}, 400

            pass_entry = Pass.query.get(pass_id)
            if not pass_entry:
                return {"error_code": 404, "message": "Pass not found"}, 404

            if pass_entry.creator_user_id != user_id:
                return {
                    "error_code": 404, 
                    "message": "This pass does not belong to the specified user"
                }, 404

            try:
                PassTraveller.query.filter_by(pass_id=pass_id).delete()
                
                db.session.delete(pass_entry)
                db.session.commit()

                return {"message": f"Pass with ID {pass_id} has been deleted successfully"}, 200

            except Exception as e:
                db.session.rollback()
                return {"error_code": 400, "message": f"Error deleting pass: {str(e)}"}, 400

    @ns_pass.route('/update')
    class UpdatePassResource(Resource):
        """Update a pass with a new date and list of travellers."""

        @api.expect(update_pass_model)
        @api.response(200, 'Pass updated successfully', pass_details_by_id_model)
        @api.response(400, 'Required fields missing or invalid date format', error_response_model_400)
        @api.response(404, 'Pass or traveller not found', error_response_model_404)
        @log_api_access('PUT /passes/update')
        def put(self):
            """Update a pass with a new date and list of travellers by passport numbers."""
            data = request.get_json()
            pass_id = data.get("pass_id")
            pass_date_str = data.get("pass_date")
            traveller_passport_numbers = data.get("traveller_passport_numbers", [])
            if not pass_id:
                return {"error_code": 400, "message": "Pass ID is required"}, 400
            
            if not pass_date_str:
                return {"error_code": 400, "message": "Pass date is required"}, 400
            
            if not isinstance(traveller_passport_numbers, list):
                return {"error_code": 400, "message": "traveller_passport_numbers must be a list"}, 400
            pass_entry = Pass.query.get(pass_id)
            if not pass_entry:
                return {"error_code": 404, "message": "Pass not found"}, 404
            try:
                new_pass_date = datetime.strptime(pass_date_str, "%Y-%m-%d %H:%M:%S")
                new_expiry_datetime = new_pass_date + timedelta(hours=24)
            except ValueError:
                return {"error_code": 400, "message": "Invalid date format. Use YYYY-MM-DD HH:MM:SS"}, 400
            travellers = []
            for passport_number in traveller_passport_numbers:
                traveller = UserSensitiveInformation.query.filter_by(passport_number=passport_number).first()
                if not traveller:
                    return {
                        "error_code": 404, 
                        "message": f"Traveller with passport number {passport_number} not found"
                    }, 404
                travellers.append(traveller)

            try:
                pass_entry.pass_date = new_pass_date
                pass_entry.expiry_datetime = new_expiry_datetime
                PassTraveller.query.filter_by(pass_id=pass_id).delete()
                travellers_list = []
                for traveller in travellers:
                    pass_traveller = PassTraveller(pass_id=pass_id, user_id=traveller.user_id)
                    db.session.add(pass_traveller)
                    travellers_list.append({
                        "user_id": traveller.user_id,
                        "first_name": traveller.first_name,
                        "middle_name": traveller.middle_name,
                        "last_name": traveller.last_name,
                        "passport_number": traveller.passport_number
                    })
                db.session.commit()
                passenger_count = len(travellers_list)
                response = {
                    "pass_id": pass_id,
                    "pass_date": pass_entry.pass_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "expiry_datetime": pass_entry.expiry_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    "pass_utilized": pass_entry.pass_utilized,
                    "passenger_count": passenger_count,
                    "travellers": travellers_list
                }

                return api.marshal(response, pass_details_by_id_model), 200

            except Exception as e:
                db.session.rollback()
                return {"error_code": 400, "message": f"Error updating pass: {str(e)}"}, 400

    @ns_pass.route('/<int:user_id>/details')
    class UserPassDetailsResource(Resource):
        """Get details for all passes created by a user."""

        @api.response(200, 'Success', pass_details_by_user_model)
        @api.response(404, 'User not found', error_response_model_404)
        @log_api_access('GET /passes/<user_id>/details')
        def get(self, user_id):
            """Retrieve details of all passes created by a user, including pass date, expiry datetime, travellers, and passenger count."""
            user = UserSensitiveInformation.query.get(user_id)
            if not user:
                return {"error_code": 404, "message": "User not found"}, 404
            pass_id = request.args.get('pass_id', None)
            passes_query = Pass.query.filter(Pass.creator_user_id == user_id)
            if pass_id is not None:
                try:
                    pass_id = int(pass_id)
                    passes_query = passes_query.filter(Pass.pass_id == pass_id)
                except ValueError:
                    return {"error_code": 400, "message": "Invalid pass_id parameter"}, 400
            
            passes = passes_query.all()
            passes_list = []
            for pass_entry in passes:
                travellers = (
                    db.session.query(
                        UserSensitiveInformation.user_id,
                        UserSensitiveInformation.first_name,
                        UserSensitiveInformation.middle_name,
                        UserSensitiveInformation.last_name,
                        UserSensitiveInformation.passport_number
                    )
                    .join(PassTraveller, UserSensitiveInformation.user_id == PassTraveller.user_id)
                    .filter(PassTraveller.pass_id == pass_entry.pass_id)
                    .all()
                )
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
                passenger_count = len(travellers_list)
                passes_list.append({
                    "pass_id": pass_entry.pass_id,
                    "pass_date": pass_entry.pass_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "expiry_datetime": pass_entry.expiry_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    "pass_utilized": pass_entry.pass_utilized,
                    "passenger_count": passenger_count,
                    "travellers": travellers_list
                })
            response = {
                "user_id": user_id,
                "passes": passes_list
            }

            return api.marshal(response, pass_details_by_user_model), 200

    return ns_pass

            