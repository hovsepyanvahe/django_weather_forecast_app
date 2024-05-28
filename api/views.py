from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from datetime import datetime, timedelta
from django.conf import settings
from .models import WeatherData
from .serializers import WeatherDataSerializer, WeatherRequestSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Define the valid detailing types
VALID_DETAILING_TYPES = ["current", "minutely", "hourly", "daily"]


class WeatherForecast(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('lat', openapi.IN_QUERY, description="Latitude", type=openapi.TYPE_NUMBER, required=True),
            openapi.Parameter('lon', openapi.IN_QUERY, description="Longitude", type=openapi.TYPE_NUMBER,
                              required=True),
            openapi.Parameter(
                'detailing_type',
                openapi.IN_QUERY,
                description="Detailing Type",
                type=openapi.TYPE_STRING,
                enum=VALID_DETAILING_TYPES,
                required=True
            )
        ],
        responses={200: WeatherDataSerializer(many=True)}
    )
    def get(self, request):
        serializer = WeatherRequestSerializer(data=request.GET)
        if serializer.is_valid():
            lat = serializer.validated_data['lat']
            lon = serializer.validated_data['lon']
            detailing_type = serializer.validated_data['detailing_type']

            all_weather_data = []
            print('detailing_types')
            to_be_excluded = [s for s in VALID_DETAILING_TYPES if s != detailing_type]
            exclude = ",".join(to_be_excluded)

            weather_data = WeatherData.objects.filter(lat=lat, lon=lon, detailing_type=detailing_type).first()

            if (weather_data and datetime.now() - weather_data.last_updated <
                    timedelta(minutes=settings.WEATHER_DATA_EXPIRY_MINUTES)):
                all_weather_data.append(weather_data)

                weather_data_serializer = WeatherDataSerializer(all_weather_data, many=True)
                return Response(weather_data_serializer.data)

            api_key = settings.OPENWEATHERMAP_API_KEY
            api_url = settings.OPENWEATHERMAP_API_URL
            url = f"{api_url}?lat={lat}&lon={lon}&exclude={exclude}&appid={api_key}"
            response = requests.get(url)

            if response.ok:
                data = response.json()
                weather_data, created = WeatherData.objects.update_or_create(
                    lat=lat, lon=lon, detailing_type=detailing_type,
                    defaults={'forecast_data': data}
                )
                all_weather_data.append(weather_data)

                weather_data_serializer = WeatherDataSerializer(all_weather_data, many=True)
                return Response(weather_data_serializer.data)
            else:
                return Response({"message": "Weather API is not responding"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
