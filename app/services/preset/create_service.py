from app import db
from app.api.models.preset import Preset, PresetTraveller
from app.api.models.user import UserSensitiveInformation
from app.utils.preset.validators import validate_preset_creation
from app.utils.preset.helpers import format_traveller_info
import logging

logger = logging.getLogger(__name__)

class PresetCreateService:
    @staticmethod
    def create_preset(user_id: int, preset_name: str, travellers: list) -> tuple:
        """
        Create a new preset with travellers.
        
        Args:
            user_id (int): ID of the user creating the preset
            preset_name (str): Name of the preset
            travellers (list): List of travellers to add to the preset
            
        Returns:
            tuple: (result dict, error message)
        """
        try:
            # Validate input
            validation_error = validate_preset_creation(user_id, preset_name, travellers)
            if validation_error:
                return None, validation_error

            # Create preset
            new_preset = Preset(preset_name=preset_name, user_id=user_id)
            db.session.add(new_preset)
            db.session.commit()

            preset_id = new_preset.preset_id
            travellers_added = []

            # Add travellers
            for traveller in travellers:
                passport_number = traveller.get("passport_number")
                user_sensitive = UserSensitiveInformation.query.filter_by(
                    passport_number=passport_number
                ).first()
                
                if not user_sensitive:
                    logger.error(f"Traveller with passport number {passport_number} not found")
                    return None, f"Traveller with passport number {passport_number} not found"

                traveller_user_id = user_sensitive.user_id
                preset_traveller = PresetTraveller(
                    preset_id=preset_id, 
                    user_id=traveller_user_id
                )
                db.session.add(preset_traveller)
                travellers_added.append(format_traveller_info(user_sensitive))

            db.session.commit()
            
            logger.info(f"Successfully created preset {preset_id} for user {user_id}")
            
            return {
                "preset_id": preset_id,
                "preset_name": preset_name,
                "created_by_user_id": user_id,
                "travellers_added": travellers_added
            }, None

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating preset: {str(e)}")
            return None, f"Error creating preset: {str(e)}" 