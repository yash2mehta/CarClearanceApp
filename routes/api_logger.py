import time
import logging
from functools import wraps
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_access.log'),
        logging.StreamHandler()
    ]
)

def log_api_access(route_name):
    """
    Decorator to log API access, start time, and end time.
    
    Args:
        route_name (str): The name of the API route being accessed
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            start_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            logging.info(f"API Access: {route_name} - Started at {start_datetime}")
            
            try:
                result = func(*args, **kwargs)
                end_time = time.time()
                duration = end_time - start_time
                end_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                logging.info(f"API Access: {route_name} - Completed at {end_datetime} - Duration: {duration:.2f} seconds")
                return result
            except Exception as e:
                end_time = time.time()
                duration = end_time - start_time
                end_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                logging.error(f"API Access: {route_name} - Failed at {end_datetime} - Duration: {duration:.2f} seconds - Error: {str(e)}")
                raise
        return wrapper
    return decorator 