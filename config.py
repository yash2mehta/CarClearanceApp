import os

# Flask configuration
UPLOAD_FOLDER = 'uploads'
SQLALCHEMY_DATABASE_URI = 'sqlite:///immigration.db'

# API configuration
API_VERSION = "1.0"
API_TITLE = "Immigration API"
API_DESCRIPTION = "A simple API for managing immigration workflows"

# Plate Recognizer API configuration
TOKEN = "210ed0449ee06e8d9bcee4a67c742814e4e7366e"
API_URL = "https://api.platerecognizer.com/v1/plate-reader/"

# Create upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER) 