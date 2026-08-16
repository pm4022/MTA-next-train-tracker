# FRONT-END ONLY
#
# The styled "departure board" version of the tracker page, served at /board.
# It calls the same data functions as the plain page in mta_routes.py and only
# changes how the results are presented.

from flask import Blueprint, render_template, request

from web_app.config import ALL_OPTION
from web_app.line_colors import (
    line_name_detail,
    load_line_colors,
    short_line_code
)
from web_app.mta_service import (
    find_station,
    get_station_arrivals,
    load_station_table
)

board_routes = Blueprint("board_routes", __name__)


@board_routes.route("/board", methods=["GET"])
def board():
    selected_station_id = request.args.get("station_id")
    selected_line = request.args.get("line")
    selected_direction = request.args.get("direction")

    stations = load_station_table()
    station = None
    arrivals = []
    error_message = None
    searched = False

    if selected_station_id:
        station = find_station(selected_station_id)

        if station is None:
            error_message = "Unsupported station."

        # Picking a station from the dropdown only puts the station in the url.
        # The line and direction only arrive once "Show next trains" is pressed,
        # so waiting for them keeps the options open while the rider chooses.
        elif selected_line and selected_direction:
            searched = True

            try:
                arrivals = get_station_arrivals(
                    selected_station_id,
                    selected_line,
                    selected_direction
                )
            except ValueError as e:
                error_message = str(e)

    # Add the extra bits each board row needs in order to be drawn
    colors = load_line_colors()

    for arrival in arrivals:
        line = arrival["line"]

        arrival["short_code"] = short_line_code(line)
        arrival["name_detail"] = line_name_detail(line)
        arrival["colors"] = colors[line]

    return render_template(
        "board.html",
        all_option=ALL_OPTION,
        stations=stations,
        station=station,
        selected_station_id=selected_station_id,
        selected_line=selected_line,
        selected_direction=selected_direction,
        arrivals=arrivals,
        error_message=error_message,
        searched=searched,
    )
