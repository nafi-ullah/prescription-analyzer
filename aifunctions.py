# aifunctions.py

import os
import openai
from flask import Flask, request, jsonify
import requests
# Retrieve API key from environment variable
API_KEY = os.getenv('OPENAI_API_KEY')
import json
# Initialize the OpenAI client
openai.api_key = API_KEY
client = openai.OpenAI()

class Medicine:
    def __init__(self, medicineName="", takingTime="", isNeedEmptyStomach="", medicineUsage="", sideEffect=""):
        self.medicineName = medicineName
        self.takingTime = takingTime
        self.isNeedEmptyStomach = isNeedEmptyStomach
        self.medicineUsage = medicineUsage
        self.sideEffect = sideEffect

class HealthData:
    def __init__(self, type="", value=""):
        self.type = type
        self.value = value

class PrescriptionAnalysis:
    def __init__(self, patientName="", age="", data=None, healthData=None, test=None):
        self.patientName = patientName
        self.age = age
        self.data = data if data is not None else []
        self.healthData = healthData if healthData is not None else []
        self.test = test if test is not None else []

import openai
import json

def get_prescription_response(prompt):
    preprompt = '''\
Only return the JSON object, without any additional text.
If you do not find any medication, return an empty array.

Here is the JSON format of your response:
{prescriptions: [{
    patientName: ,
    age: ,
    data: [{
        medicineName: ,
        takingTime: 1+1+0,
        isNeedEmptyStomach: no-yes-x,
        medicineUsage: ,
        sideEffect: 
    }],
    healthData: [{
        type: ,
        value: 
    }],
    test: [test 1, test 2]
}]}
Where:
- patientName: Should contain the patient's name.
- age: Should contain the patient's age.
- data: An array of objects that contains the medicine details.
- healthData: An array of objects that contains health-related information.
- test: An array of strings listing any tests associated with the prescription.
'''

    if not prompt:
        return []

    # Concatenate prompt and preprompt
    full_prompt = prompt + "\n\n" + preprompt

    # Call the OpenAI API
    completion = openai.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": full_prompt}
        ]
    )
    print("GPT call done")

    # Check the content before parsing
    raw_content = json.loads(completion.choices[0].message.content)["prescriptions"]
    print("Raw API Response:")
    print(raw_content)

    # Process the raw response to fit the expected format
    processed_content = []
    
    for prescription in raw_content:
        # Initialize medicines
        medicines = []
        for med in prescription.get("data", []):
            try:
                medicines.append(Medicine(**med))
            except Exception as e:
                print(f"Skipping invalid medicine data: {med}. Error: {e}")

        # Initialize health data, skipping any problematic entries
        health_data = []
        for health in prescription.get("healthData", []):
            try:
                health_data.append(HealthData(**health))
            except Exception as e:
                print(f"Skipping invalid health data: {health}. Error: {e}")

        prescription_analysis = PrescriptionAnalysis(
            patientName=prescription.get("patientName", "PATIENT NAME NOT FOUND"),
            age=prescription.get("age", "AGE NOT FOUND"),
            data=medicines,
            healthData=health_data,
            test=prescription.get("test", [])
        )
        processed_content.append(prescription_analysis.__dict__)

    print("Processed response_content:")
    for item in processed_content:
        item['data'] = [med.__dict__ for med in item['data']]  # Convert Medicine instances to dictionaries
        item['healthData'] = [health.__dict__ for health in item['healthData']]  # Convert HealthData instances to dictionaries

    print(processed_content)

    return processed_content



def analyze_image_and_prompt(image_url, prompt):
    # Prepare the request to GPT-4o-mini
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    
    if response.choices and response.choices[0].message:
        print(response.choices[0].message.content)
        return response.choices[0].message.content
    else:
        return {'error': 'Failed to analyze the image and prompt.'}

def generate_dalle_image(analysis, image):
    # Prepare the prompt by combining analysis and image description
    prompt = f"{analysis}. The image reference is: {image}"

    # Generate the image using the OpenAI client
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    
    # Return the generated image URL
    return response.data[0].url



