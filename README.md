# MTA-next-train-tracker

 A focused tracker could give riders faster access to the information they need to decide when to leave or which train to take.

Pick a station, then subway line and direction, and the app shows the next three
arrivals with their expected times and minutes away, using the MTA's live
GTFS-Realtime feeds.

## Setup

Install the package dependencies (from the root directory of this repo):

```sh
pip install -r requirements.txt
```

## Usage

Run the local web server, then visit http://127.0.0.1:5000/board in a browser:

```sh
FLASK_APP=web_app flask run
```

> NOTE: the first station lookup for each server run takes a few seconds while
> the MTA's static station data downloads. It is cached in memory after that.

Arrival times are displayed in New York time, because that is the timezone the
subway runs on. The "minutes away" values are calculated from timestamps, so
they are correct regardless of where you are running the app.

## Project Structure

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

The MTA feed configuration and the data retrieval and processing pipeline were
written by the project team, as recorded in this repo's earlier commit history.

This application structure is adapted from the prof's
[Flask Sheets Template 2024](https://github.com/prof-rossetti/flask-sheets-template-2024),
with the Google OAuth login and Google Sheets database layers removed, since
this app has no user accounts and reads from a public API instead of a database.

### AI assistance

The front-end was AI-assisted: everything in `web_app/templates/`.

## Data Sources

  * [MTA Developer Resources](https://www.mta.info/developers) — official MTA static and real-time data.
  * [MTA Real-Time Data Feeds](https://api.mta.info/) — the GTFS-Realtime feeds used for live arrivals.
  * [MTA GTFS Documentation](https://github.com/nymta/gtfs-documentation) — route, station, and real-time field documentation.
  * [GTFS-Realtime Reference](https://gtfs.org/documentation/realtime/reference/) — the standard real-time transit data format.
  * [GTFS-Realtime Python Bindings](https://pypi.org/project/gtfs-realtime-bindings/) — decodes the MTA's Protocol Buffer data.
