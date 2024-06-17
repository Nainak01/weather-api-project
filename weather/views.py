from drf_yasg import openapi
from django.http import Http404
from .models import Record, Stats
from rest_framework.mixins import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import GenericViewSet
from .serializers import RecordSerializer, StatsSerializer
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND


class RecordViewSet(ListModelMixin, GenericViewSet):
    """ViewSet for listing Record instances."""

    queryset = Record.objects.all()
    serializer_class = RecordSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "date",
                openapi.IN_QUERY,
                description="Date of the record",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
            ),
            openapi.Parameter(
                "station",
                openapi.IN_QUERY,
                description="Name of the station",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def list(self, request):
        """List records with optional filtering by date and station."""
        try:
            date = request.GET.get("date", None)
            station_name = request.GET.get("station", None)

            if date:
                self.queryset = self.queryset.filter(date=date)
            if station_name:
                self.queryset = self.queryset.filter(station__name=station_name)

            page = self.paginate_queryset(self.queryset)

            if not page:
                raise Http404("No records found matching the criteria")

            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        except Http404 as e:
            return Response({"error": str(e)}, status=HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response({"error": str(error)}, status=HTTP_400_BAD_REQUEST)


class StatsViewSet(ListModelMixin, GenericViewSet):
    """ViewSet for listing Stats instances."""

    queryset = Stats.objects.all()
    serializer_class = StatsSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "year",
                openapi.IN_QUERY,
                description="Year of the stats",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "station",
                openapi.IN_QUERY,
                description="Name of the station",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def list(self, request):
        """List stats with optional filtering by year and station."""
        try:
            year = request.GET.get("year", None)
            station_name = request.GET.get("station", None)

            if year:
                self.queryset = self.queryset.filter(year=year)
            if station_name:
                self.queryset = self.queryset.filter(station__name=station_name)

            page = self.paginate_queryset(self.queryset)

            if not page:
                raise Http404("No stats found matching the criteria")

            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        except Http404 as e:
            return Response({"error": str(e)}, status=HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response({"error": str(error)}, status=HTTP_400_BAD_REQUEST)
