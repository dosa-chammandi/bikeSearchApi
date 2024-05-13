# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire current directory into the container
COPY . .

# Expose port 80 to allow communication with the outside world
EXPOSE 8080

# Command to run the FastAPI application when the container starts
CMD ["python", "app/main.py"]
