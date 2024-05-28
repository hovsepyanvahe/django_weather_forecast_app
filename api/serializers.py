from rest_framework import serializers
from .models import WeatherData


class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = '__all__'


class WeatherRequestSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lon = serializers.FloatField()
    detailing_type = serializers.CharField()

    VALID_DETAILING_TYPES = {"current", "minutely", "hourly", "daily"}

    def validate_detailing_types(self, value):
        detailing_type = value.split(',')
        invalid_types = [type_ for type_ in detailing_type if type_ not in self.VALID_DETAILING_TYPES]
        if invalid_types:
            raise serializers.ValidationError(
                f"Invalid detailing types: {', '.join(invalid_types)}. Valid types are: {', '.join(self.VALID_DETAILING_TYPES)}.")
        return detailing_type
