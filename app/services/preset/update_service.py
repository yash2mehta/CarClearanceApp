from app import db
from app.api.models.preset import Preset, PresetTraveller
from app.api.models.user import UserSensitiveInformation
from app.utils.preset.validators import validate_preset_update
from app.utils.preset.helpers import format_traveller_info
import logging

logger = logging.getLogger(__name__)

class PresetUpdateService:
    @staticmethod
    def update_preset_name(user_id: int, preset_id: int, new_name: str) -> tuple:
        """
        Update the name of a preset.
        
        Args:
            user_id (int): ID of the user
            preset_id (int): ID of the preset to update
            new_name (str): New name for the preset
            
        Returns:
            tuple: (result dict, error message)
        """
        try:
            validation_error = validate_preset_update(user_id, preset_id)
            if validation_error:
                return None, validation_error

            preset = Preset.query.get(preset_id)
            preset.preset_name = new_name
            db.session.commit()

            logger.info(f"Successfully updated preset {preset_id} name to {new_name}")
            
            return {
                "preset_id": preset_id,
                "preset_name": new_name,
                "message": "Preset name updated successfully"
            }, None

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating preset name: {str(e)}")
            return None, f"Error updating preset name: {str(e)}"

    @staticmethod
    def update_preset_travellers(user_id: int, preset_id: int, traveller_ids: list) -> tuple:
        """
        Update the travellers in a preset.
        
        Args:
            user_id (int): ID of the user
            preset_id (int): ID of the preset to update
            traveller_ids (list): List of traveller IDs to add to the preset
            
        Returns:
            tuple: (result dict, error message)
        """
        try:
            validation_error = validate_preset_update(user_id, preset_id)
            if validation_error:
                return None, validation_error

            # Remove existing travellers
            PresetTraveller.query.filter_by(preset_id=preset_id).delete()

            # Add new travellers
            travellers_added = []
            for traveller_id in traveller_ids:
                traveller = UserSensitiveInformation.query.get(traveller_id)
                if not traveller:
                    logger.error(f"Traveller {traveller_id} not found")
                    return None, f"Traveller {traveller_id} not found"

                preset_traveller = PresetTraveller(
                    preset_id=preset_id,
                    user_id=traveller_id
                )
                db.session.add(preset_traveller)
                travellers_added.append(format_traveller_info(traveller))

            db.session.commit()

            logger.info(f"Successfully updated travellers for preset {preset_id}")
            
            return {
                "preset_id": preset_id,
                "travellers_added": travellers_added,
                "message": "Preset travellers updated successfully"
            }, None

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating preset travellers: {str(e)}")
            return None, f"Error updating preset travellers: {str(e)}" 