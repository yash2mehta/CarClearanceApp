from app import db
from app.api.models.preset import Preset, PresetTraveller
from app.api.models.user import UserSensitiveInformation
from app.utils.preset.helpers import format_traveller_info
import logging

logger = logging.getLogger(__name__)

class PresetReadService:
    @staticmethod
    def get_preset_summary(user_id: int) -> tuple:
        """
        Get summary of all presets for a user.
        
        Args:
            user_id (int): ID of the user
            
        Returns:
            tuple: (result dict, error message)
        """
        try:
            user = UserSensitiveInformation.query.get(user_id)
            if not user:
                logger.error(f"User {user_id} not found")
                return None, "User not found"

            presets = Preset.query.filter_by(user_id=user_id).all()
            presets_list = []

            for preset in presets:
                passenger_count = db.session.query(PresetTraveller).filter_by(
                    preset_id=preset.preset_id
                ).count()
                
                presets_list.append({
                    "preset_id": preset.preset_id,
                    "preset_name": preset.preset_name,
                    "passenger_count": passenger_count,
                    "created_at": preset.created_at,
                    "updated_at": preset.updated_at
                })

            return {
                "user_id": user_id,
                "presets": presets_list
            }, None

        except Exception as e:
            logger.error(f"Error getting preset summary: {str(e)}")
            return None, f"Error getting preset summary: {str(e)}"

    @staticmethod
    def get_preset_details(preset_id: int) -> tuple:
        """
        Get detailed information about a specific preset.
        
        Args:
            preset_id (int): ID of the preset
            
        Returns:
            tuple: (result dict, error message)
        """
        try:
            preset = Preset.query.get(preset_id)
            if not preset:
                logger.error(f"Preset {preset_id} not found")
                return None, "Preset not found"

            travellers = (
                db.session.query(UserSensitiveInformation)
                .join(PresetTraveller)
                .filter(PresetTraveller.preset_id == preset_id)
                .all()
            )

            travellers_list = [format_traveller_info(t) for t in travellers]

            return {
                "preset_id": preset.preset_id,
                "preset_name": preset.preset_name,
                "created_by_user_id": preset.user_id,
                "passenger_count": len(travellers_list),
                "travellers": travellers_list,
                "created_at": preset.created_at,
                "updated_at": preset.updated_at
            }, None

        except Exception as e:
            logger.error(f"Error getting preset details: {str(e)}")
            return None, f"Error getting preset details: {str(e)}" 