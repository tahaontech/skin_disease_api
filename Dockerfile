# Use the official Python base image
FROM python:3.9-slim

# Create a working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the entire application to the working directory
COPY . .

# Expose the port the app runs on
EXPOSE 8585

# Set the entry point for the container
CMD ["python", "app.py"]
