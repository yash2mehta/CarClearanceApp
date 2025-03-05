from flask import Flask, request
API_URL = "https://api.platerecognizer.com/v1/plate-reader/" # This is the PlateRecognizer API Url

# Function to recognize license plate using PlateRecognizer API
def recognize_license_plate(image_path, token):

    # Create headers dictionary for authentication
    headers = {
        "Authorization": f"Token {token}"
    }

    with open(image_path, "rb") as fp:

        # Send request to Plate Recognizer
        response = requests.post(API_URL, headers=headers, files={"upload": fp})
        
        # If request was successful
        if response.status_code == 200 or response.status_code == 201:
            
            data = response.json()
            if data['results']:
                
                # Extract license plate from the response
                return data['results'][0]['plate']
            
            else:
                return "No license plate detected."
        
        else:
            return f"Error: {response.status_code}, {response.text}"


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # return redirect(url_for('static', filename='uploads/' + filename), code=301)

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

