# License Plate Detection System User Guide

## 1. Overview

This server is a Flask-based web application that provides multiple API endpoints for managing immigration workflows that is useful for the Car Clearance App. This server provides a RESTful API interface for all operations and includes features for:
- Vehicle management
- User management
- Pass management
- Preset management
- Traveller management

In addition to the API endpoints, this system uses SQLite as its database.

## 2. Installation & Setup

### Prerequisites
- Python 3.x
- pip (Python package manager)
- Git (optional, for version control)

### Installation Steps

1. Clone the repository (if using Git):
   ```bash
   git clone [repository-url]
   cd [repository-directory]
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   .\env\Scripts\activate # On Windows
   source env/bin/activate # On macOS/Linux
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create the uploads directory (if not automatically created):
   ```bash
   mkdir uploads
   ```

## 3. Running the System

1. Ensure you're in the project directory and the virtual environment is activated.
2. Start the server: `python main.py`
3. The server will start on:
   - Host: 0.0.0.0
   - Port: 5000
   - Debug mode: Enabled
4. Access the API at:
   - http://localhost:5000
5. The system will automatically:
   - Initialize the database
   - Create all necessary tables
   - Insert mock data for testing

## 4. Possible Errors & Troubleshooting

### Common Issues and Solutions

#### 1. Port Already in Use
- Error: "Address already in use"
- Solution:
  - Find and kill the process using port 5000
  - Or change the port in main.py

#### 2. Database Issues
- Error: "Database not found" or "Table not found"
- Solution:
  - Ensure the database file (immigration.db) is not locked
  - Delete the database file and restart the server

#### 3. Missing Dependencies
- Error: "Module not found"
- Solution:
  - Ensure all requirements are installed: `pip install -r requirements.txt`
  - Check Python version compatibility

#### 4. Upload Directory Issues
- Error: "Upload directory not found"
- Solution:
  - Create the uploads directory manually
  - Ensure proper write permissions

## 5. Additional Notes

- The system runs in debug mode by default, which provides detailed error messages
- All API endpoints are documented and can be accessed through the Swagger UI at /
- The system uses SQLite, so no additional database server is required
- Mock data is automatically inserted on server start for testing purposes

---

*This guide provides a comprehensive overview of the Web Scraper system designed for Vaxtor. For additional support or specific issues, please contact the development team.* 