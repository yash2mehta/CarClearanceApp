from app.api.models.user import UserSensitiveInformation
from app.api.models.preset import Preset
import logging

logger = logging.getLogger(__name__)

def validate_preset_creation(user_id: int, preset_name: str, travellers: list) -> str:
    """
    Validate preset creation input.
    
    Args:
        user_id (int): ID of the user creating the preset
        preset_name (str): Name of the preset
        travellers (list): List of travellers to add to the preset
        
    Returns:
        str: Error message if validation fails, None if validation passes
    """
    # Validate user exists
    user = UserSensitiveInformation.query.get(user_id)
    if not user:
        logger.error(f"User {user_id} not found")
        return "User not found"

    # Validate preset name
    if not preset_name or not isinstance(preset_name, str):
        logger.error("Invalid preset name")
        return "Preset name is required and must be a string"

    # Validate travellers
    if not travellers or not isinstance(travellers, list):
        logger.error("Invalid travellers list")
        return "At least one traveller is required"

    for traveller in travellers:
        if not isinstance(traveller, dict):
            logger.error("Invalid traveller format")
            return "Each traveller must be a dictionary"
            
        passport_number = traveller.get("passport_number")
        if not passport_number or not isinstance(passport_number, str):
            logger.error("Invalid passport number")
            return "Each traveller must have a valid passport number"

    return None

def validate_preset_update(user_id: int, preset_id: int) -> str:
    """
    Validate preset update input.
    
    Args:
        user_id (int): ID of the user
        preset_id (int): ID of the preset to update
        
    Returns:
        str: Error message if validation fails, None if validation passes
    """
    # Validate user exists
    user = UserSensitiveInformation.query.get(user_id)
    if not user:
        logger.error(f"User {user_id} not found")
        return "User not found"

    # Validate preset exists
    preset = Preset.query.get(preset_id)
    if not preset:
        logger.error(f"Preset {preset_id} not found")
        return "Preset not found"

    # Validate user owns the preset
    if preset.user_id != user_id:
        logger.error(f"User {user_id} does not own preset {preset_id}")
        return "This preset does not belong to the specified user"

    return None

def validate_preset_delete(user_id: int, preset_id: int) -> str:
    """
    Validate preset deletion input.
    
    Args:
        user_id (int): ID of the user
        preset_id (int): ID of the preset to delete
        
    Returns:
        str: Error message if validation fails, None if validation passes
    """
    # Validate user exists
    user = UserSensitiveInformation.query.get(user_id)
    if not user:
        logger.error(f"User {user_id} not found")
        return "User not found"

    # Validate preset exists
    preset = Preset.query.get(preset_id)
    if not preset:
        logger.error(f"Preset {preset_id} not found")
        return "Preset not found"

    # Validate user owns the preset
    if preset.user_id != user_id:
        logger.error(f"User {user_id} does not own preset {preset_id}")
        return "This preset does not belong to the specified user"

    return None 