from flask import Blueprint, render_template, request

from web_app.config import LINE_OPTIONS
from web_app.mta_service import get_stations_for_line, get_next_arrivals

mta_routes = Blueprint("mta_routes", __name__)


@mta_routes.route("/", methods=["GET"])
def index():
    selected_line = request.args.get("line")
    selected_station_id = request.args.get("station_id")
    selected_direction = request.args.get("direction")

    stations = []
    arrivals = []
    error_message = None

    if selected_line:
        stations = get_stations_for_line(selected_line)

        if selected_station_id and selected_direction:
            try:
                arrivals = get_next_arrivals(
                    selected_line, selected_station_id, selected_direction
                )
            except ValueError as e:
                error_message = str(e)

    return render_template(
        "index.html",
        lines=LINE_OPTIONS.keys(),
        selected_line=selected_line,
        selected_station_id=selected_station_id,
        selected_direction=selected_direction,
        stations=stations,
        arrivals=arrivals,
        error_message=error_message,
    )
