# Use the official Python image from the Docker Hub.
FROM python:3.10-slim

# Set environment variables.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory.
WORKDIR /app

# Install dependencies.
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the application code.
COPY . /app/

# Expose port 8000 to the outside world.
EXPOSE 8000

# Command to run the application.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "weather.wsgi:application"]
