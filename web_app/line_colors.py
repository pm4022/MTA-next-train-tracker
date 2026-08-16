# FRONT-END ONLY
#
# Works out what colour to draw each subway line bullet in on the styled
# board page. The colours are read from the MTA's own routes.txt file, so
# they are the official ones.

from web_app.config import (
    DEFAULT_LINE_COLOR,
    DEFAULT_LINE_TEXT_COLOR,
    LINE_OPTIONS
)
from web_app.mta_service import load_static_gtfs


# Variable to store the colours
line_colors = None


def clean_color(value, fallback):
# Turn color from the MTA file into something a browser understands

    # Missing values come back from pandas as a number, not a string
    if not isinstance(value, str):
        return fallback

    value = value.strip()

    if value == "":
        return fallback

    return "#" + value


def load_line_colors():
# Build a lookup of line name to the colors its bullet should use

    global line_colors

    if line_colors is None:
        routes = load_static_gtfs()["routes"]
        rows = routes.to_dict("records")

        # First collect the colors the MTA gives for each route id
        colors_by_route = {}

        for row in rows:
            colors_by_route[row["route_id"]] = {
                "background": clean_color(
                    row.get("route_color"),
                    DEFAULT_LINE_COLOR
                ),
                "text": clean_color(
                    row.get("route_text_color"),
                    DEFAULT_LINE_TEXT_COLOR
                )
            }

        # Then turn those route ids into the line names the app shows
        colors = {}

        for line in LINE_OPTIONS:
            colors[line] = {
                "background": DEFAULT_LINE_COLOR,
                "text": DEFAULT_LINE_TEXT_COLOR
            }

            for route_id in LINE_OPTIONS[line]["route_ids"]:
                if route_id in colors_by_route:
                    colors[line] = colors_by_route[route_id]
                    break

        line_colors = colors

    return line_colors


def short_line_code(line):
# The shuttles have long names, so use just the letter inside the bullet

    if " - " in line:
        return line.split(" - ")[0]

    return line


def line_name_detail(line):
# The rest of a shuttle's name, shown next to the bullet

    if " - " in line:
        return line.split(" - ")[1]

    return ""
