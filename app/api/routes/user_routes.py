from flask_restx import Namespace, Resource
from flask import request
from app.services.user_service import UserService
from app.api.schemas import (
    user_profile_model, user_profile_with_id_model,
    error_response_model_400, error_response_model_404
)

ns_user = Namespace('users', description='User-related operations')

@ns_user.route('/<int:user_id>/profile')
class UserProfileResource(Resource):
    """Retrieve the profile of the user."""

    @ns_user.response(200, 'User profile retrieved successfully', user_profile_model)
    @ns_user.response(404, 'User not found', error_response_model_404)
    def get(self, user_id):
        """Get all the information of the user."""
        profile = UserService.get_user_profile(user_id)
        if not profile:
            return {"error_code": 404, "message": "User not found"}, 404
        return profile, 200

@ns_user.route('/<int:user_id>/update-profile')
class UpdateUserProfileResource(Resource):
    """Update user profile information."""

    @ns_user.expect(user_profile_model)
    @ns_user.response(200, 'User profile updated successfully', user_profile_with_id_model)
    @ns_user.response(400, 'Invalid data format', error_response_model_400)
    @ns_user.response(404, 'User ID not found', error_response_model_404)
    def put(self, user_id):
        data = request.get_json()
        try:
            updated_user = UserService.update_user_profile(user_id, data)
            if not updated_user:
                return {"error_code": 404, "message": "User not found"}, 404
            
            return UserService.get_user_profile(user_id), 200
        except Exception as e:
            return {"error_code": 400, "message": f"Error updating user profile: {str(e)}"}, 400 