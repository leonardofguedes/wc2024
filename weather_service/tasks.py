import requests
import logging
import redis
from celery import shared_task
from django.conf import settings
from .models import WeatherData
import time

logger = logging.getLogger(__name__)

OPEN_WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'
UNITS = 'metric'
redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)  # Atualize aqui

@shared_task(bind=True)
def fetch_weather_data(self, user_id, city_ids):
    api_key = settings.OPEN_WEATHER_API_KEY

    if not api_key:
        logger.error("Open Weather API key is not set.")
        return

    total_cities = len(city_ids)
    redis_key_progress = f"weather_progress_{user_id}"
    redis_key_total = f"weather_total_{user_id}"
    progress = 0

    redis_client.set(redis_key_total, total_cities)
    redis_client.set(redis_key_progress, progress)
    
    
    # Store the total number of cities in Redis
    redis_client.set(redis_key_total, total_cities)
    
    for i, city_id in enumerate(city_ids):
        if i > 0 and i % 60 == 0:
            # Wait for a minute before making the next batch of requests
            time.sleep(60)
        
        weather_data = get_weather_data(api_key, city_id)
        if weather_data:
            save_weather_data(user_id, city_id, weather_data)
        # Update progress
        progress = (i + 1)
        redis_client.set(redis_key_progress, progress)

    redis_client.delete(redis_key_progress)  # Remove the progress tracking once done
    redis_client.delete(redis_key_total)  # Remove the total tracking once done

def get_weather_data(api_key, city_id):
    try:
        response = requests.get(OPEN_WEATHER_URL, params={
            'id': city_id,
            'appid': api_key,
            'units': UNITS
        })
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred for city_id {city_id}: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        logger.error(f"Connection error occurred for city_id {city_id}: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        logger.error(f"Timeout error occurred for city_id {city_id}: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Error fetching weather data for city_id {city_id}: {req_err}")
    return None

def save_weather_data(user_id, city_id, data):
    weather_data, created = WeatherData.objects.update_or_create(
        user_id=user_id,
        city_id=city_id,
        defaults={
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'data': data
        }
    )

    if created:
        logger.info(f"Weather data collected for city_id: {city_id}")
    else:
        logger.info(f"Weather data for city_id: {city_id} already exists")
