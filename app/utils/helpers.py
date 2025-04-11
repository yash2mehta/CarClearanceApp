from datetime import datetime, timedelta

def format_datetime(dt):
    """Format datetime object to string."""
    if isinstance(dt, datetime):
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return dt

def calculate_expiry_datetime(pass_date):
    """Calculate expiry datetime based on pass date."""
    if isinstance(pass_date, str):
        pass_date = datetime.strptime(pass_date, "%Y-%m-%d %H:%M:%S")
    return pass_date + timedelta(hours=24)

def format_user_name(first_name, middle_name, last_name):
    """Format user's full name."""
    name_parts = []
    if first_name:
        name_parts.append(first_name)
    if middle_name:
        name_parts.append(middle_name)
    if last_name:
        name_parts.append(last_name)
    return " ".join(name_parts)

def format_traveller_info(traveller):
    """Format traveller information for response."""
    return {
        "user_id": traveller.user_id,
        "first_name": traveller.first_name,
        "middle_name": traveller.middle_name,
        "last_name": traveller.last_name,
        "passport_number": traveller.passport_number
    } 