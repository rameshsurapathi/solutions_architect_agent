
# Dockerfile for a Python application

# Base image
FROM python:3.9-slim

# Working directory
# This is where the application code will be copied to and run from
WORKDIR /app

# Copy requirements.txt to the working directory
COPY requirements.txt .

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# This installs the dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files from the current directory to the working directory in the container
# This includes the application code and any other necessary files
COPY . .

# Expose the port the app runs on
# This is the port that the application will listen on
EXPOSE 8080

# Command to run the application
# This command will be executed when the container starts
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
