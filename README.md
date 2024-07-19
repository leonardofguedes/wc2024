# wc2024

## Weather Service Application

This project is a Weather Service Application built with Django, Celery, Redis, and Docker. 
It collects weather data from the Open Weather API and provides an API to retrieve this data.

Ensure you have the following installed on your system:
```
Docker
Docker Compose
Python3
```
Installation

Clone the repository:
```
git clone https://github.com/leonardofguedes/wc2024.git
```

Create a .env file in the root directory and add the following environment variables:

```
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
OPEN_WEATHER_API_KEY=your_open_weather_api_key
```

Running the Application
Build and run the Docker containers:

```
docker-compose up --build
```


This will build the Docker images and start the application with all the necessary services (Django, Celery, Redis).

Apply database migrations:

Once the containers are up and running, open a new terminal and run:

```
docker-compose exec web python manage.py migrate
```

Usage

The Django application will be available at http://localhost:8000.

Celery is used to handle asynchronous tasks such as fetching weather data.
Redis is used as the message broker for Celery.

API Endpoints

POST api/weather: Collect weather data from the Open Weather API and store it.

Request Body:
json
```
{
  "user_id": "unique_user_id",
  "city_ids": [12345, 67890]
}
```

GET api/weather/{user_id}: Get the progress of the weather data collection for a specific user.

Response:
```
{
  "progress_percentage": 75.0,
  "total_cities": 4,
  "progress": 3
}
```

## Libraries Used

### Django: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
### Django Rest Framework (DRF): A powerful and flexible toolkit for building Web APIs.
### Celery: An asynchronous task queue/job queue based on distributed message passing.
### Redis: An in-memory data structure store, used as a message broker for Celery.
### Gunicorn: A Python WSGI HTTP server for UNIX.
### Requests: A simple, yet elegant HTTP library for Python.
