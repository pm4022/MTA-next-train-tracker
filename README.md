# MTA-next-train-tracker

 A focused tracker could give riders faster access to the information they need to decide when to leave or which train to take.

Pick a subway line, station, and direction, and the app shows you the next three
trains, along with when each one gets there and how many minutes away it is.

## Setup

From the project's main folder, install what the app needs:

```sh
pip install -r requirements.txt
```

## Usage

Start the app, then open http://127.0.0.1:5000 in your browser:

```sh
FLASK_APP=web_app flask run
```

## Project Structure

The app serves two versions of the same tracker. The plain page is at `/` and a
styled, dark "departure board" version is at `/board`. Both read the same data.

```
web_app/
  __init__.py                    # starts up the Flask app
  config.py                      # which feed and route ids belong to each line
  mta_service.py                 # gets the MTA data and pulls out the arrivals
  line_colors.py                 # line bullet colours, read from the MTA data
  routes/
    mta_routes.py                # runs the plain page at /
    board_routes.py              # runs the styled board page at /board
  templates/
    bootstrap_5_layout.html      # shared page layout for the plain page
    index.html                   # the plain tracker page
    board_layout.html            # dark page layout for the board page
    board.html                   # the styled board page
```

## Attribution

Built on top of the prof's
[Flask Sheets Template 2024](https://github.com/prof-rossetti/flask-sheets-template-2024).
The Google login and Google Sheets parts were dropped, since this app has no
accounts and reads from a public API instead of a database.

## Data Sources

  * [MTA Developer Resources](https://www.mta.info/developers) — official MTA static and real-time data.
  * [MTA Real-Time Data Feeds](https://api.mta.info/) — the GTFS-Realtime feeds used for live arrivals.
  * [MTA GTFS Documentation](https://github.com/nymta/gtfs-documentation) — route, station, and real-time field documentation.
  * [GTFS-Realtime Reference](https://gtfs.org/documentation/realtime/reference/) — the standard real-time transit data format.
  * [GTFS-Realtime Python Bindings](https://pypi.org/project/gtfs-realtime-bindings/) — decodes the MTA's Protocol Buffer data.
