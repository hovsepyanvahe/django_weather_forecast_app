from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
from .models import WeatherData


class WeatherForecastTests(APITestCase):
    def test_weather_forecast_endpoint(self):
        url = reverse('weather-forecast')
        data = {'lat': 33.441792, 'lon': -94.037689, 'detailing_type': 'current'}

        with patch('requests.get') as mock_get:
            mock_response = mock_get.return_value
            mock_response.status_code = 200
            mock_response.json.return_value = {'weather': 'data'}

            response = self.client.get(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]['lat'], 33.441792)
        self.assertEqual(response.json()[0]['lon'], -94.037689)

        # Check if WeatherData is created
        weather_data = WeatherData.objects.first()
        self.assertIsNotNone(weather_data)
        self.assertEqual(weather_data.lat, 33.441792)
        self.assertEqual(weather_data.lon, -94.037689)
        self.assertEqual(weather_data.detailing_type, 'current')

    def test_invalid_weather_forecast_request(self):
        url = reverse('weather-forecast')
        data = {'lat': 33.441792, 'lon': -94.037689}  # Missing detailing_type

        response = self.client.get(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
