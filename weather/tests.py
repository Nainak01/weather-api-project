from django.urls import reverse
from .models import Record, Stats, Station
from rest_framework.test import APIClient, APITestCase
from .serializers import RecordSerializer, StatsSerializer
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND


class RecordTest(APITestCase):
    """Tests for /weather endpoint."""

    def setUp(self):
        """Set up test data for Record model tests."""
        self.client = APIClient()
        self.route = reverse("weather-list")

        station_list = [Station.objects.create(name=f"Test{i}") for i in range(1, 3)]

        Record.objects.create(
            date="1985-01-01",
            max_temp=-22,
            min_temp=-128,
            precipitation=94,
            station=station_list[0],
        ),
        Record.objects.create(
            date="1985-01-02",
            max_temp=-122,
            min_temp=-217,
            precipitation=0,
            station=station_list[0],
        ),
        Record.objects.create(
            date="1985-01-03",
            max_temp=-106,
            min_temp=-244,
            precipitation=0,
            station=station_list[0],
        ),
        Record.objects.create(
            date="1986-01-10",
            max_temp=-11,
            min_temp=-67,
            precipitation=25,
            station=station_list[1],
        ),
        Record.objects.create(
            date="1986-01-11",
            max_temp=-11,
            min_temp=-67,
            precipitation=20,
            station=station_list[1],
        ),
        Record.objects.create(
            date="1986-01-17",
            max_temp=11,
            min_temp=-61,
            precipitation=41,
            station=station_list[1],
        )

        Stats.objects.create(
            avg_max_temp=-8.3,
            avg_min_temp=-19,
            total_precipitation=0.94,
            year=1985,
            station=station_list[0],
        ),
        Stats.objects.create(
            avg_max_temp=-11,
            avg_min_temp=-13,
            total_precipitation=0.28,
            year=1986,
            station=station_list[1],
        )

    def test_list_record(self):
        """Test listing all records."""
        response = self.client.get(self.route, content_type="application/json")
        records = Record.objects.all()
        serializer = RecordSerializer(records, many=True)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(response.data["results"], serializer.data)

    def test_list_record_with_date_filter(self):
        """Test listing records with a date filter."""
        date_filter = "1985-01-03"
        response = self.client.get(
            f"{self.route}?date={date_filter}", content_type="application/json"
        )
        records = Record.objects.filter(date=date_filter)
        serializer = RecordSerializer(records, many=True)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(response.data["count"], len(serializer.data))

    def test_list_record_with_station_filter(self):
        """Test listing records with a station filter."""
        station = "Test1"
        response = self.client.get(
            f"{self.route}?station={station}", content_type="application/json"
        )
        records = Record.objects.filter(station__name=station)
        serializer = RecordSerializer(records, many=True)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(response.data["count"], len(serializer.data))

    def test_list_record_with_wrong_filter(self):
        """Test listing records with an incorrect filter."""
        station = "Wrong-Station"
        date = "2025-01-01"
        response = self.client.get(
            f"{self.route}?station={station}&date={date}",
            content_type="application/json",
        )
        records = Record.objects.filter(station__name=station, date=date)
        serializer = RecordSerializer(records, many=True)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
        self.assertEqual(response["Content-Type"], "application/json")


class StatsTest(APITestCase):
    """Tests for /weather/stats endpoint."""

    def setUp(self):
        """Set up test data for Stats model tests."""
        self.client = APIClient()
        self.route = reverse("weather-stats-list")

        station_list = [Station.objects.create(name=f"Test{i}") for i in range(1, 3)]

        Stats.objects.create(
            avg_max_temp=-8.3,
            avg_min_temp=-19,
            total_precipitation=0.94,
            year=1985,
            station=station_list[0],
        ),
        Stats.objects.create(
            avg_max_temp=-11,
            avg_min_temp=-13,
            total_precipitation=0.28,
            year=1986,
            station=station_list[1],
        )

    def test_list_stats(self):
        """Test listing all stats."""
        response = self.client.get(self.route, content_type="application/json")
        stats = Stats.objects.all()
        serializer = StatsSerializer(stats, many=True)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(response.data["results"], serializer.data)

    def test_list_stats_with_year_filter(self):
        """Test listing stats with a year filter."""
        year_filter = "1985"
        response = self.client.get(
            f"{self.route}?year={year_filter}", content_type="application/json"
        )
        stats = Stats.objects.filter(year=year_filter)
        serializer = StatsSerializer(stats, many=True)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(response.data["count"], len(serializer.data))

    def test_list_stats_with_station_filter(self):
        """Test listing stats with a station filter."""
        station = "Test1"
        response = self.client.get(
            f"{self.route}?station={station}", content_type="application/json"
        )
        stats = Stats.objects.filter(station__name=station)
        serializer = StatsSerializer(stats, many=True)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(response.data["count"], len(serializer.data))

    def test_list_stats_with_wrong_filter(self):
        """Test listing stats with an incorrect filter."""
        station = "Wrong-Station"
        year = 2024
        response = self.client.get(
            f"{self.route}?station={station}&year={year}",
            content_type="application/json",
        )
        stats = Stats.objects.filter(station__name=station, year=year)
        serializer = RecordSerializer(stats, many=True)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
        self.assertEqual(response["Content-Type"], "application/json")
