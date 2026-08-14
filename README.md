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

```
web_app/
  __init__.py                    # starts up the Flask app
  config.py                      # which feed and route ids belong to each line
  mta_service.py                 # gets the MTA data and pulls out the arrivals
  routes/
    mta_routes.py                # runs the page and calls mta_service
  templates/
    bootstrap_5_layout.html      # shared page layout
    index.html                   # the tracker page itself
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
