# Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose a port if your application had one (not strictly necessary for this crawler)
# EXPOSE 8000

# Define environment variables (optional, but good practice)
ENV PYTHONUNBUFFERED=1

# No CMD here, as we'll use 'docker run' with specific commands for each mode.
# This keeps the image flexible.