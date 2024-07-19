from django.urls import path
from .views import WeatherDataView

urlpatterns = [
    path('weather/', WeatherDataView.as_view(), name='weatherdata'),
    path('weather/<str:user_id>/', WeatherDataView.as_view(), name='weatherdata-detail'),
]
