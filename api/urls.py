from django.urls import path
from .views import WeatherForecast

urlpatterns = [
    path('weather/', WeatherForecast.as_view(), name='weather-forecast'),
]