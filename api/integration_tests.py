# integration_tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from datetime import timedelta
from django.utils import timezone
from .models import WeatherData


class WeatherForecastIntegrationTests(TestCase):
    def test_weather_forecast_integration(self):
        url = reverse('weather-forecast')
        data = {'lat': 33.441792, 'lon': -94.037689, 'detailing_type': 'current'}

        with patch('requests.get') as mock_get:
            mock_response = mock_get.return_value
            mock_response.status_code = 200
            mock_response.json.return_value = {'weather': 'data'}

            response = self.client.get(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'weather': 'data'})

        weather_data = WeatherData.objects.first()
        self.assertIsNotNone(weather_data)
        self.assertEqual(weather_data.lat, 33.441792)
        self.assertEqual(weather_data.lon, -94.037689)
        self.assertEqual(weather_data.detailing_type, 'current')
        self.assertEqual(weather_data.forecast_data, {'weather': 'data'})

        # Ensure the cache is utilized
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'weather': 'data'})
