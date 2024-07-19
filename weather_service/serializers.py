from rest_framework import serializers
from .models import WeatherData

class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = ['user_id', 'datetime', 'city_id', 'temperature', 'humidity', 'data']
