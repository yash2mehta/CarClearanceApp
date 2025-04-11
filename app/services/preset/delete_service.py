from app import db
from app.api.models.preset import Preset, PresetTraveller
from app.utils.preset.validators import validate_preset_delete
import logging

logger = logging.getLogger(__name__)

class PresetDeleteService:
    @staticmethod
    def delete_preset(user_id: int, preset_id: int) -> tuple:
        """
        Delete a preset and its associated travellers.
        
        Args:
            user_id (int): ID of the user
            preset_id (int): ID of the preset to delete
            
        Returns:
            tuple: (result dict, error message)
        """
        try:
            validation_error = validate_preset_delete(user_id, preset_id)
            if validation_error:
                return None, validation_error

            # Delete preset travellers (cascade will handle this, but we do it explicitly for logging)
            PresetTraveller.query.filter_by(preset_id=preset_id).delete()
            
            # Delete the preset
            preset = Preset.query.get(preset_id)
            db.session.delete(preset)
            db.session.commit()

            logger.info(f"Successfully deleted preset {preset_id}")
            
            return {
                "message": f"Preset with ID {preset_id} has been deleted successfully"
            }, None

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting preset: {str(e)}")
            return None, f"Error deleting preset: {str(e)}" 