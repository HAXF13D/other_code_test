# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory
WORKDIR /usr/src/

# Copy the requirements file and install the dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port that the FastAPI app runs on
EXPOSE 8000

ENV PYTHONPATH="${PYTHONPATH}:/usr/src/app"
