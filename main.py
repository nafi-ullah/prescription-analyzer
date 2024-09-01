from flask import Flask, request, jsonify, send_from_directory
import requests
import json
import os
from PIL import Image
from datetime import datetime
from aifunctions import analyze_image_and_prompt, generate_dalle_image
import cloudinary
import cloudinary.uploader
import cloudinary.api
cloudinary.config( 
    cloud_name = "dyftlrfdk", 
    api_key = "647463598268291", 
    api_secret = "gliW0U9VhfYVhMaTtKvnNIwjkbc", # Click 'View API Keys' above to copy your API secret
    secure=True
)

app = Flask(__name__)

UPLOAD_FOLDER = './uploads/'


os.makedirs(UPLOAD_FOLDER, exist_ok=True)


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

 


@app.route('/generate-image', methods=['POST'])
def generate_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    image = request.files['image']
    
    if image.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Upload the image directly to Cloudinary
    upload_result = cloudinary.uploader.upload(image, public_id=f"{os.path.splitext(image.filename)[0]}")
    
    # Get the secure URL of the uploaded image
    uploaded_image_path = upload_result["secure_url"]
    
    print(uploaded_image_path)

    analysis_promt = """
    Describe the following prescription image medications . You have to describe the tests if it mentioned in prescription.  
    
     Here is the JSON format of your response: 
    {
"medicines" : [{
 "medicine_name" : ""  ,
 "one_line_short_description": "" ,
 "description":  "",
 "medicine_time": [] , // breakfast, lunch, dinner
 "is_take_after_meal":  // true or false
},
...
...

]
 "test" : [{
  "test_name": "",
  "one_line_short_description": "",
  "description": ""
 },
 ..
 ..
 ..
 ]

}
    """
    
    
    if not uploaded_image_path or not analysis_promt:
        return jsonify({'error': 'Image and prompt are required.'}), 400
  
    gpt_analysis = analyze_image_and_prompt(uploaded_image_path, analysis_promt)
    #image_prompt = f"You have to change the background of the car. The car should be infront of hyundai car shop. The image description is: {gpt_analysis}."
    print(gpt_analysis)
    # generated_image = generate_dalle_image(image_prompt, uploaded_image_path)
    # print(generated_image)
    # return jsonify({'generated_image': generated_image})
    

if __name__ == '__main__':
    create_version_file()
    app.run(port=5000)


