def format_traveller_info(traveller) -> dict:
    """
    Format traveller information into a standardized dictionary.
    
    Args:
        traveller: UserSensitiveInformation object
        
    Returns:
        dict: Formatted traveller information
    """
    return {
        "user_id": traveller.user_id,
        "first_name": traveller.first_name,
        "middle_name": traveller.middle_name,
        "last_name": traveller.last_name,
        "passport_number": traveller.passport_number
    }

def format_preset_info(preset, include_travellers: bool = False) -> dict:
    """
    Format preset information into a standardized dictionary.
    
    Args:
        preset: Preset object
        include_travellers (bool): Whether to include traveller information
        
    Returns:
        dict: Formatted preset information
    """
    preset_info = {
        "preset_id": preset.preset_id,
        "preset_name": preset.preset_name,
        "created_by_user_id": preset.user_id,
        "created_at": preset.created_at,
        "updated_at": preset.updated_at
    }

    if include_travellers:
        preset_info["travellers"] = [
            format_traveller_info(t.traveller) for t in preset.travellers
        ]
        preset_info["passenger_count"] = len(preset_info["travellers"])

    return preset_info 