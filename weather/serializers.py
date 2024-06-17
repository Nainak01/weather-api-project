from .models import *
from rest_framework import serializers


class RecordSerializer(serializers.ModelSerializer):
    """Serializer for the Record model."""

    station = serializers.SerializerMethodField()

    @staticmethod
    def get_station(obj):
        return obj.station.name

    class Meta:
        model = Record
        fields = (
            "id",
            "date",
            "max_temp",
            "min_temp",
            "precipitation",
            "station",
        )


class StatsSerializer(serializers.ModelSerializer):
    """Serializer for the Stats model."""

    station = serializers.SerializerMethodField()

    @staticmethod
    def get_station(obj):
        return obj.station.name

    class Meta:
        model = Stats
        fields = (
            "id",
            "avg_max_temp",
            "avg_min_temp",
            "total_precipitation",
            "year",
            "station",
        )
