from flask import Flask, request, jsonify, send_from_directory
import requests
import json
import os
from PIL import Image
from datetime import datetime
from aifunctions import analyze_image_and_prompt, generate_dalle_image, get_prescription_response
import cloudinary
import cloudinary.uploader
import cloudinary.api
import re
cloudinary.config( 
    cloud_name = "dyftlrfdk", 
    api_key = "647463598268291", 
    api_secret = "gliW0U9VhfYVhMaTtKvnNIwjkbc", # Click 'View API Keys' above to copy your API secret
    secure=True
)

app = Flask(__name__)

UPLOAD_FOLDER = './uploads/'


os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def clean_and_convert_to_json(response_string):
    # Use regex to remove the ```json and ``` block and any escape sequences
    cleaned_response_string = re.sub(r'```json|```', '', response_string).strip()
    
    # Debug: Print the cleaned string
    print("Cleaned Response String:", cleaned_response_string)
    
    try:
        # Parse the cleaned string as a JSON object
        json_object = json.loads(cleaned_response_string)
        return json_object
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return response_string
    
def create_version_file():
    # Get the current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Define the JSON data
    data = {
        "time": current_time
    }
    # Write the JSON data to a file
    with open('version_check.json', 'w') as json_file:
        json.dump(data, json_file)

def get_version_time():
    # Check if the file exists
    if os.path.exists('version_check.json'):
        # Read the JSON file
        with open('version_check.json', 'r') as json_file:
            data = json.load(json_file)
            return data.get("time")
    else:
        return None

@app.route('/check', methods=['GET'])
def check():
    # Get the time from the JSON file
    version_time = get_version_time()
    if version_time:
        return jsonify(message=f"Hello, it's working updated at {version_time}")
    else:
        return jsonify(message="Version time not found"), 404


@app.route('/uploaded_images/<filename>')
def get_result_image1(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

 


@app.route('/analysis-prescription', methods=['POST'])
def generate_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    image = request.files['image']
    
    if image.filename == '':
        return jsonify({'error': 'No file selected.'}), 400
    
    try:
        # Upload the image directly to Cloudinary
        upload_result = cloudinary.uploader.upload(image, public_id=f"{os.path.splitext(image.filename)[0]}")
    
        # Get the secure URL of the uploaded image
        uploaded_image_path = upload_result["secure_url"]
        print(f"Uploaded image path: {uploaded_image_path}")
    except Exception as e:
        print(f"Error uploading image: {str(e)}")
        return jsonify({'error': 'Failed to upload image.', 'details': str(e)}), 500

    analysis_prompt = """
    Describe the following prescription image medications. You have to describe the tests if mentioned in the prescription.
    include medicine names, taking times, isNeedEmptyStomach, medicine usage, side effects, health related datas, patient name, age, test data etc.
    """
    
    if not uploaded_image_path or not analysis_prompt:
        return jsonify({'error': 'Image and prompt are required.'}), 400

    # Call the function to analyze the image and get the result
    gpt_analysis = analyze_image_and_prompt(uploaded_image_path, analysis_prompt)
    
    # DEBUG: Log the exact GPT response for debugging purposes
    print("GPT Analysis Raw Response:", gpt_analysis)
    
    # Attempt to clean up the response (e.g., remove extraneous characters or text)
  
        # Sometimes GPT might return some leading or trailing text that is not part of the JSON
    json_output = get_prescription_response(gpt_analysis)
        
        # Ensure only valid JSON is returned
        # gpt_analysis_json = json.loads(gpt_analysis_cleaned)
    
    
    print("GPT Analysis Parsed JSON:", json_output)
    
    # Return the parsed JSON as a response
    return jsonify(json_output)
    

if __name__ == '__main__':
    create_version_file()
    app.run(port=5000)


