# aifunctions.py

import os
import openai
from flask import Flask, request, jsonify
import requests
# Retrieve API key from environment variable
API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI client
openai.api_key = API_KEY
client = openai.OpenAI()

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
