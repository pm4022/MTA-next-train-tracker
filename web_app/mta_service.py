# Functions for retrieving and processing MTA subway data

import io
import math
import time
import zipfile
from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
import requests
from google.transit import gtfs_realtime_pb2

from web_app.config import ALL_OPTION, LINE_OPTIONS, STATIC_GTFS_URL


# This variable stores the downloaded data so it is not downloaded repeatedly.
static_gtfs_tables = None

# This variable stores the station list so it is only built once.
station_table = None


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


def filter_arrivals(
    records,
    selected_line,
    station_id,
    direction,
    current_timestamp=None
):
# Filter, format, and return the next three matching trains

    if selected_line not in LINE_OPTIONS:
        raise ValueError("Unsupported subway line.")

    if direction not in ("N", "S"):
        raise ValueError("Direction must be N or S.")

    if current_timestamp is None:
        current_timestamp = time.time()

    route_ids = LINE_OPTIONS[selected_line]["route_ids"]
    selected_stop_id = f"{station_id}{direction}"
    upcoming_arrivals = []

    for record in records:
        if record["route_id"] not in route_ids:
            continue

        if record["stop_id"] != selected_stop_id:
            continue

        if record["arrival_timestamp"] <= current_timestamp:
            continue

        minutes_away = math.ceil(
            (record["arrival_timestamp"] - current_timestamp) / 60
        )

        arrival_time = datetime.fromtimestamp(
            record["arrival_timestamp"],
            ZoneInfo("America/New_York")
        ).strftime("%I:%M %p").lstrip("0")

        upcoming_arrivals.append({
            "line": selected_line,
            "station_id": station_id,
            "direction": direction,
            "expected_arrival": arrival_time,
            "minutes_away": minutes_away,
            "arrival_timestamp": record["arrival_timestamp"]
        })

    upcoming_arrivals.sort(
        key=lambda arrival: arrival["arrival_timestamp"]
    )

    return upcoming_arrivals[:3]


def get_next_arrivals(selected_line, station_id, direction):
# Connect all live arrival functions into one function

    feed = fetch_realtime_feed(selected_line)
    records = extract_arrival_records(feed)

    return filter_arrivals(
        records,
        selected_line,
        station_id,
        direction
    )


def route_ids_to_lines():
# Map the MTA's route ids back to the line names shown to riders

    mapping = {}

    for line in LINE_OPTIONS:
        for route_id in LINE_OPTIONS[line]["route_ids"]:
            mapping[route_id] = line

    return mapping


def load_station_table():
# Build the list of every station, with the lines that stop there

    global station_table

    if station_table is None:
        tables = load_static_gtfs()
        route_to_line = route_ids_to_lines()

        trips = tables["trips"]
        stop_times = tables["stop_times"]
        stops = tables["stops"]

        # Only keep trips running on lines this app supports
        known_route_ids = []

        for route_id in route_to_line:
            known_route_ids.append(route_id)

        known_trips = trips[trips["route_id"].isin(known_route_ids)]

        route_stops = stop_times.merge(
            known_trips,
            on="trip_id"
        )

        route_stops = route_stops[
            ["route_id", "stop_id"]
        ].drop_duplicates()

        route_stops = route_stops.merge(
            stops,
            on="stop_id"
        )

        route_stops["station_id"] = route_stops[
            "parent_station"
        ].fillna(route_stops["stop_id"])

        rows = route_stops.to_dict("records")

        # Collect the lines that stop at each station
        stations_by_id = {}

        for row in rows:
            station_id = row["station_id"]
            line = route_to_line[row["route_id"]]

            if station_id not in stations_by_id:
                stations_by_id[station_id] = {
                    "station_id": station_id,
                    "stop_name": row["stop_name"],
                    "lines": []
                }

            station = stations_by_id[station_id]

            if line not in station["lines"]:
                station["lines"].append(line)

        stations = []

        for station_id in stations_by_id:
            station = stations_by_id[station_id]
            station["lines"].sort()

            station["label"] = (
                station["stop_name"] + " - " + ", ".join(station["lines"])
            )

            stations.append(station)

        stations.sort(key=lambda station: station["label"])

        station_table = stations

    return station_table


def find_station(station_id):
# Look up a single station by its id

    for station in load_station_table():
        if station["station_id"] == station_id:
            return station

    return None


def fetch_feed_from_url(feed_url):
# Download and decode one live feed, given its url

    response = requests.get(feed_url, timeout=30)
    response.raise_for_status()

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    return feed


def get_station_arrivals(
    station_id,
    selected_line=None,
    direction=None,
    limit=3,
    current_timestamp=None
):
# Return the soonest trains at a station, optionally filtered by line and direction

    station = find_station(station_id)

    if station is None:
        raise ValueError("Unsupported station.")

    # A blank or "All" line means every line that stops here
    if selected_line in (None, "", ALL_OPTION):
        lines = station["lines"]
    elif selected_line in station["lines"]:
        lines = [selected_line]
    else:
        raise ValueError("That line does not stop at this station.")

    # A blank or "All" direction means both directions
    if direction in (None, "", ALL_OPTION):
        directions = ["N", "S"]
    elif direction in ("N", "S"):
        directions = [direction]
    else:
        raise ValueError("Direction must be N or S.")

    # Work out which route ids to keep and which feeds to download
    route_ids = []
    feed_urls = []

    for line in lines:
        for route_id in LINE_OPTIONS[line]["route_ids"]:
            if route_id not in route_ids:
                route_ids.append(route_id)

        feed_url = LINE_OPTIONS[line]["feed_url"]

        if feed_url not in feed_urls:
            feed_urls.append(feed_url)

    # A platform stop id is the station id plus the direction letter
    wanted_stop_ids = []

    for one_direction in directions:
        wanted_stop_ids.append(station_id + one_direction)

    # A station can be served by lines from more than one feed
    records = []

    for feed_url in feed_urls:
        feed = fetch_feed_from_url(feed_url)

        for record in extract_arrival_records(feed):
            records.append(record)

    if current_timestamp is None:
        current_timestamp = time.time()

    route_to_line = route_ids_to_lines()
    upcoming_arrivals = []

    for record in records:
        if record["route_id"] not in route_ids:
            continue

        if record["stop_id"] not in wanted_stop_ids:
            continue

        if record["arrival_timestamp"] <= current_timestamp:
            continue

        minutes_away = math.ceil(
            (record["arrival_timestamp"] - current_timestamp) / 60
        )

        arrival_time = datetime.fromtimestamp(
            record["arrival_timestamp"],
            ZoneInfo("America/New_York")
        ).strftime("%I:%M %p").lstrip("0")

        upcoming_arrivals.append({
            "line": route_to_line[record["route_id"]],
            "station_id": station_id,
            "stop_name": station["stop_name"],
            "direction": record["stop_id"][-1],
            "expected_arrival": arrival_time,
            "minutes_away": minutes_away,
            "arrival_timestamp": record["arrival_timestamp"]
        })

    upcoming_arrivals.sort(
        key=lambda arrival: arrival["arrival_timestamp"]
    )

    return upcoming_arrivals[:limit]
