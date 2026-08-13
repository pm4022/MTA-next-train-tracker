# Functions for retrieving and processing MTA subway data

import io
import zipfile

import pandas as pd
import requests
from google.transit import gtfs_realtime_pb2

from web_app.config import LINE_OPTIONS, STATIC_GTFS_URL


# This variable stores the downloaded data so it is not downloaded repeatedly.
static_gtfs_tables = None


def load_static_gtfs():
# Download and read the MTA station and schedule files

    global static_gtfs_tables

    if static_gtfs_tables is None:
        response = requests.get(STATIC_GTFS_URL, timeout=30)
        response.raise_for_status()

        gtfs_zip = zipfile.ZipFile(io.BytesIO(response.content))

        trips = pd.read_csv(
            gtfs_zip.open("trips.txt"),
            usecols=["route_id", "trip_id"]
        )

        stop_times = pd.read_csv(
            gtfs_zip.open("stop_times.txt"),
            usecols=["trip_id", "stop_id"]
        )

        stops = pd.read_csv(
            gtfs_zip.open("stops.txt"),
            usecols=["stop_id", "stop_name", "parent_station"],
            dtype=str
        )

        static_gtfs_tables = {
            "trips": trips,
            "stop_times": stop_times,
            "stops": stops
        }

    return static_gtfs_tables


def get_stations_for_line(selected_line):
# Return all stations served by the selected subway line

    if selected_line not in LINE_OPTIONS:
        return []

    tables = load_static_gtfs()

    route_ids = LINE_OPTIONS[selected_line]["route_ids"]
    trips = tables["trips"]
    stop_times = tables["stop_times"]
    stops = tables["stops"]

    matching_trips = trips[trips["route_id"].isin(route_ids)]

    matching_stop_times = stop_times.merge(
        matching_trips,
        on="trip_id"
    )

    matching_stops = matching_stop_times.merge(
        stops,
        on="stop_id"
    )

    matching_stops["station_id"] = matching_stops[
        "parent_station"
    ].fillna(matching_stops["stop_id"])

    station_rows = matching_stops[
        ["station_id", "stop_name"]
    ].drop_duplicates()

    station_rows = station_rows.sort_values("stop_name")

    stations = station_rows.to_dict("records")

    return stations


def fetch_realtime_feed(selected_line):
# Download and decode the live feed for a selected subway line

    if selected_line not in LINE_OPTIONS:
        raise ValueError("Unsupported subway line.")

    feed_url = LINE_OPTIONS[selected_line]["feed_url"]

    response = requests.get(feed_url, timeout=30)
    response.raise_for_status()

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    return feed


def extract_arrival_records(feed):
# Convert the live feed into simple arrival dictionaries

    arrival_records = []

    for entity in feed.entity:
        if not entity.HasField("trip_update"):
            continue

        trip_update = entity.trip_update
        route_id = trip_update.trip.route_id

        for stop_update in trip_update.stop_time_update:
            arrival_time = stop_update.arrival.time

            if arrival_time == 0:
                arrival_time = stop_update.departure.time

            if arrival_time == 0:
                continue

            arrival_records.append({
                "route_id": route_id,
                "stop_id": stop_update.stop_id,
                "arrival_timestamp": arrival_time
            })

    return arrival_records
    