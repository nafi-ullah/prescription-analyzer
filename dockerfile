# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    libgl1-mesa-glx \
    libglib2.0-0

COPY requirements.txt .
RUN pip install --upgrade pip
# Install the Python dependencies
RUN pip install --upgrade pip
RUN pip install Flask
RUN pip install flask_cors 
RUN pip install scraper openai 
RUN pip install python-dotenv
RUN pip install requests
RUN pip install gunicorn
RUN pip install Pillow
#RUN pip install rembg
RUN pip install cloudinary
RUN pip install numpy
#RUN pip install opencv-python
#RUN pip install -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .


# Expose the port on which the Flask app will run
EXPOSE 5055

# Set the entrypoint command to run the Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "admin:app", "--timeout", "180"]
# CMD ["python", "main.py"]
