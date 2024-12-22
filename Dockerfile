# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Expose port 8080 (default for Cloud Run)
EXPOSE 8080

# Command to run the app
CMD ["uvicorn", "main:create_api", "--host", "0.0.0.0", "--port", "8080"]
