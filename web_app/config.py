# Configuration data for the MTA Next Train Tracker

# Value used by the dropdowns when the rider does not want to filter
ALL_OPTION = "All"

# Used for the line bullets when the MTA feed does not give a colour
DEFAULT_LINE_COLOR = "#808183"
DEFAULT_LINE_TEXT_COLOR = "#ffffff"

BASE_URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds"
STATIC_GTFS_URL = "https://rrgtfsfeeds.s3.amazonaws.com/gtfs_subway.zip"

FEED_URLS = {
    "123456S": f"{BASE_URL}/nyct%2Fgtfs",
    "7": f"{BASE_URL}/nyct%2Fgtfs-7",
    "ACE": f"{BASE_URL}/nyct%2Fgtfs-ace",
    "BDFM": f"{BASE_URL}/nyct%2Fgtfs-bdfm",
    "G": f"{BASE_URL}/nyct%2Fgtfs-g",
    "JZ": f"{BASE_URL}/nyct%2Fgtfs-jz",
    "NQRW": f"{BASE_URL}/nyct%2Fgtfs-nqrw",
    "L": f"{BASE_URL}/nyct%2Fgtfs-l",
    "SIR": f"{BASE_URL}/nyct%2Fgtfs-si"
}

LINE_OPTIONS = {
    "1": {"route_ids": ["1"], "feed_url": FEED_URLS["123456S"]},
    "2": {"route_ids": ["2"], "feed_url": FEED_URLS["123456S"]},
    "3": {"route_ids": ["3"], "feed_url": FEED_URLS["123456S"]},
    "4": {"route_ids": ["4"], "feed_url": FEED_URLS["123456S"]},
    "5": {"route_ids": ["5"], "feed_url": FEED_URLS["123456S"]},
    "6": {"route_ids": ["6", "6X"], "feed_url": FEED_URLS["123456S"]},
    "7": {"route_ids": ["7", "7X"], "feed_url": FEED_URLS["7"]},
    "A": {"route_ids": ["A"], "feed_url": FEED_URLS["ACE"]},
    "B": {"route_ids": ["B"], "feed_url": FEED_URLS["BDFM"]},
    "C": {"route_ids": ["C"], "feed_url": FEED_URLS["ACE"]},
    "D": {"route_ids": ["D"], "feed_url": FEED_URLS["BDFM"]},
    "E": {"route_ids": ["E"], "feed_url": FEED_URLS["ACE"]},
    "F": {"route_ids": ["F", "FX"], "feed_url": FEED_URLS["BDFM"]},
    "G": {"route_ids": ["G"], "feed_url": FEED_URLS["G"]},
    "J": {"route_ids": ["J"], "feed_url": FEED_URLS["JZ"]},
    "L": {"route_ids": ["L"], "feed_url": FEED_URLS["L"]},
    "M": {"route_ids": ["M"], "feed_url": FEED_URLS["BDFM"]},
    "N": {"route_ids": ["N"], "feed_url": FEED_URLS["NQRW"]},
    "Q": {"route_ids": ["Q"], "feed_url": FEED_URLS["NQRW"]},
    "R": {"route_ids": ["R"], "feed_url": FEED_URLS["NQRW"]},
    "W": {"route_ids": ["W"], "feed_url": FEED_URLS["NQRW"]},
    "Z": {"route_ids": ["Z"], "feed_url": FEED_URLS["JZ"]},
    "S - 42 St": {
        "route_ids": ["GS"],
        "feed_url": FEED_URLS["123456S"]
    },
    "S - Franklin Av": {
        "route_ids": ["FS"],
        "feed_url": FEED_URLS["ACE"]
    },
    "S - Rockaway Park": {
        "route_ids": ["H"],
        "feed_url": FEED_URLS["ACE"]
    },
    "SIR": {"route_ids": ["SI"], "feed_url": FEED_URLS["SIR"]}
}