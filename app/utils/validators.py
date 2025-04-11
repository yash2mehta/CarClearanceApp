from datetime import datetime

def validate_date(date_str, date_format="%Y-%m-%d"):
    """Validate if a string is a valid date in the specified format."""
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False

def validate_datetime(datetime_str, datetime_format="%Y-%m-%d %H:%M:%S"):
    """Validate if a string is a valid datetime in the specified format."""
    try:
        datetime.strptime(datetime_str, datetime_format)
        return True
    except ValueError:
        return False

def validate_passport_number(passport_number):
    """Validate passport number format."""
    # Basic validation - can be enhanced based on specific requirements
    if not passport_number or len(passport_number) < 5:
        return False
    return True

def validate_vehicle_number(vehicle_number):
    """Validate vehicle number format."""
    # Basic validation - can be enhanced based on specific requirements
    if not vehicle_number or len(vehicle_number) < 3:
        return False
    return True 