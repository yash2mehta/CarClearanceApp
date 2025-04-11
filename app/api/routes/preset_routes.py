from flask_restx import Namespace, Resource
from flask import request
from app.services.preset_service import PresetService
from app.api.schemas import (
    preset_details_model, preset_with_users_model,
    error_response_model_400, error_response_model_404,
    success_message_model
)

ns_preset = Namespace('presets', description='Preset-related operations')

@ns_preset.route('/<int:user_id>/create-preset')
class CreatePresetResource(Resource):
    """Create a new preset with travellers."""

    @ns_preset.expect(preset_with_users_model)
    @ns_preset.response(200, 'Preset created successfully', preset_with_users_model)
    @ns_preset.response(400, 'Missing required fields', error_response_model_400)
    @ns_preset.response(404, 'User or traveller not found', error_response_model_404)
    def post(self, user_id):
        """Create a new preset with travellers."""
        data = request.get_json()
        preset_name = data.get('preset_name')
        travellers = data.get('travellers', [])

        if not preset_name:
            return {"error_code": 400, "message": "Preset name is required"}, 400

        if not travellers:
            return {"error_code": 400, "message": "At least one traveller is required"}, 400

        result, error = PresetService.create_preset(user_id, preset_name, travellers)
        if error:
            if error == "User not found":
                return {"error_code": 404, "message": error}, 404
            return {"error_code": 400, "message": error}, 400

        return result, 200

@ns_preset.route('/<int:user_id>/get-all-presets')
class UserPresetsResource(Resource):
    """Get all presets for a user."""

    @ns_preset.response(200, 'Success', preset_details_model)
    @ns_preset.response(404, 'User not found', error_response_model_404)
    def get(self, user_id):
        """Retrieve all presets for a user."""
        result, error = PresetService.get_preset_summary(user_id)
        if error:
            return {"error_code": 404, "message": error}, 404
        return result, 200

@ns_preset.route('/<int:user_id>/delete-preset/<int:preset_id>')
class DeletePresetResource(Resource):
    """Delete a preset."""

    @ns_preset.response(200, 'Preset deleted successfully', success_message_model)
    @ns_preset.response(404, 'User or preset not found', error_response_model_404)
    def delete(self, user_id, preset_id):
        """Delete a preset and its associated travellers."""
        result, error = PresetService.delete_preset(user_id, preset_id)
        if error:
            if error == "User not found" or error == "Preset not found":
                return {"error_code": 404, "message": error}, 404
            return {"error_code": 400, "message": error}, 400

        return result, 200 