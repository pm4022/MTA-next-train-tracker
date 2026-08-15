from flask import Blueprint, render_template, request

from web_app.config import ALL_OPTION
from web_app.mta_service import (
    find_station,
    get_station_arrivals,
    load_station_table
)

mta_routes = Blueprint("mta_routes", __name__)


@mta_routes.route("/", methods=["GET"])
def index():
    selected_station_id = request.args.get("station_id")
    selected_line = request.args.get("line")
    selected_direction = request.args.get("direction")

    stations = load_station_table()
    station = None
    arrivals = []
    error_message = None

    if selected_station_id:
        station = find_station(selected_station_id)

        if station is None:
            error_message = "Unsupported station."
        else:
            try:
                arrivals = get_station_arrivals(
                    selected_station_id,
                    selected_line,
                    selected_direction
                )
            except ValueError as e:
                error_message = str(e)

    return render_template(
        "index.html",
        all_option=ALL_OPTION,
        stations=stations,
        station=station,
        selected_station_id=selected_station_id,
        selected_line=selected_line,
        selected_direction=selected_direction,
        arrivals=arrivals,
        error_message=error_message,
    )
