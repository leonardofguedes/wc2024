from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import redis
from .models import WeatherData
from .serializers import WeatherDataSerializer
from .tasks import fetch_weather_data
from django.conf import settings


redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0) 
class WeatherDataView(APIView):

    def post(self, request, format=None):
        user_id = request.data.get('user_id')
        city_ids = request.data.get('city_ids')

        if not user_id or not city_ids:
            return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar se o user_id já existe no banco de dados
        if WeatherData.objects.filter(user_id=user_id).exists():
            return Response({"error": "user_id already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Iniciar a tarefa assíncrona para coletar dados meteorológicos
        fetch_weather_data.delay(user_id, city_ids)
        return Response({"message": "Data collection started"}, status=status.HTTP_201_CREATED)

    def get(self, request, user_id, format=None):
        redis_key_progress = f"weather_progress_{user_id}"
        redis_key_total = f"weather_total_{user_id}"
        
        total_cities = redis_client.get(redis_key_total)
        progress = redis_client.get(redis_key_progress)
        
        if total_cities is None or progress is None:
            weather_data = WeatherData.objects.filter(user_id=user_id)
            if not weather_data.exists():
                return Response({"error": "Data not found"}, status=status.HTTP_404_NOT_FOUND)
            progress_percentage = 100.0
            total_cities = total_cities if total_cities is not None else 0
            progress = progress if progress is not None else 0
        else:
            total_cities = int(total_cities)
            progress = int(progress)
            progress_percentage = (progress / total_cities) * 100 if total_cities > 0 else 0

        return Response({
            "progress percentage": progress_percentage,
            'total-cities': total_cities,
            'progress': progress
        }, status=status.HTTP_200_OK)
