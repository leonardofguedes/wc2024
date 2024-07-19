from django.db import models

class WeatherData(models.Model):
    user_id = models.CharField(max_length=255)
    datetime = models.DateTimeField(auto_now_add=True)
    city_id = models.IntegerField()
    temperature = models.FloatField()
    humidity = models.IntegerField()
    data = models.JSONField()

    def __str__(self):
        return f"{self.user_id} - {self.city_id}"

