import os
import logging
from pathlib import Path
from weather.models import *
from datetime import datetime
from django.db import transaction
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Script to load the data into database"

    def handle(self, *args, **options):
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s",
            filename="script.log",
        )

        start_time = datetime.now()
        folder_path = "data/wx_data"

        try:
            file_list = os.listdir(folder_path)

            with transaction.atomic():
                for file_name in file_list:
                    if file_name.endswith(".txt"):
                        file_path = os.path.join(folder_path, file_name)
                        weather_data_list = []
                        station_name = Path(file_path).stem

                        station, created = Station.objects.get_or_create(
                            name=station_name
                        )

                        with open(file_path, "r") as file:
                            for line in file:
                                data = line.strip().split("\t")
                                if "-9999" in data:
                                    continue
                                try:
                                    date = datetime.strptime(data[0], "%Y%m%d").date()
                                    max_temp = int(data[1].strip())
                                    min_temp = int(data[2].strip())
                                    precipitation = int(data[3].strip())
                                except ValueError:
                                    logging.warning(
                                        f"Skipping invalid data line: {line}"
                                    )
                                    continue

                                weather_data_list.append(
                                    Record(
                                        date=date,
                                        station=station,
                                        max_temp=max_temp,
                                        min_temp=min_temp,
                                        precipitation=precipitation,
                                    )
                                )

                        Record.objects.bulk_create(weather_data_list)

                        year_stats = {}
                        for weather_data in weather_data_list:
                            year = weather_data.date.year
                            if year not in year_stats:
                                year_stats[year] = {
                                    "max_temp_sum": 0,
                                    "min_temp_sum": 0,
                                    "precipitation_sum": 0,
                                    "count": 0,
                                }
                            year_stats[year]["max_temp_sum"] += weather_data.max_temp
                            year_stats[year]["min_temp_sum"] += weather_data.min_temp
                            year_stats[year][
                                "precipitation_sum"
                            ] += weather_data.precipitation
                            year_stats[year]["count"] += 1

                        # Create or update Stats objects
                        weather_stats_list = []
                        for year, stats in year_stats.items():
                            avg_max_temp = stats["max_temp_sum"] / (stats["count"] * 10)
                            avg_min_temp = stats["min_temp_sum"] / (stats["count"] * 10)
                            total_precipitation = stats["precipitation_sum"] / 100
                            weather_stats_list.append(
                                Stats(
                                    year=year,
                                    station=station,
                                    avg_max_temp=avg_max_temp,
                                    avg_min_temp=avg_min_temp,
                                    total_precipitation=total_precipitation,
                                )
                            )

                        Stats.objects.bulk_create(weather_stats_list)

                        end_time = datetime.now()
                        logging.info(
                            f"Start time {start_time}, End time {end_time}, Inserted Record Records {len(weather_data_list)}, Inserted Stats Records {len(weather_stats_list)}"
                        )

        except Exception as e:
            logging.error(str(e))
