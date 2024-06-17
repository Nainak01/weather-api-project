from django.db import models
from django.db.models import Index


class Station(models.Model):
    """Model representing a weather station."""

    name = models.CharField(verbose_name="Name of Station", unique=True, max_length=100)

    def __str__(self):
        return self.name


class Record(models.Model):
    """Model representing a weather record for a specific station and date."""

    date = models.DateField(verbose_name="Record Date", null=True, blank=True)
    max_temp = models.IntegerField(
        verbose_name="Maximum Temperature", null=True, blank=True
    )
    min_temp = models.IntegerField(
        verbose_name="Minimum Temperature", null=True, blank=True
    )
    precipitation = models.IntegerField(
        verbose_name="Precipitation", null=True, blank=True
    )
    station = models.ForeignKey(
        Station, on_delete=models.CASCADE, verbose_name="Station ID"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["date", "station"], name="unique_date_station"
            )
        ]
        indexes = [Index(fields=["date", "station"], name="index_date_station")]
        ordering = ["-id"]

    def __str__(self):
        return f"Record for {self.station.name} on {self.date}"


class Stats(models.Model):
    """Model representing yearly weather statistics for a specific station."""

    avg_max_temp = models.FloatField(verbose_name="Average Maximum Temperature")
    avg_min_temp = models.FloatField(verbose_name="Average Minimum Temperature")
    total_precipitation = models.FloatField(verbose_name="Total Precipitation")
    year = models.IntegerField(verbose_name="Record Year")
    station = models.ForeignKey(
        Station, on_delete=models.CASCADE, verbose_name="Station ID"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["year", "station"], name="unique_year_station"
            )
        ]
        indexes = [Index(fields=["year", "station"], name="index_year_station")]
        ordering = ["-id"]

    def __str__(self):
        return f"Record for {self.station.name} on {self.year}"
