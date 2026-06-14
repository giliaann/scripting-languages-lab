import sqlite3
import sys
from pathlib import Path


def create_stops_table(cursor: sqlite3.Cursor) -> None:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stops (
            stop_id TEXT PRIMARY KEY,
            stop_code TEXT,
            stop_name TEXT NOT NULL,
            stop_lat REAL NOT NULL,
            stop_lon REAL NOT NULL
        )
    """)


def create_routes_table(cursor: sqlite3.Cursor) -> None:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS routes (
            route_id TEXT PRIMARY KEY,
            agency_id TEXT NOT NULL,
            route_short_name TEXT,
            route_long_name TEXT,
            route_desc TEXT,
            route_type INTEGER NOT NULL
        )
    """)


def create_calendar_table(cursor: sqlite3.Cursor) -> None:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calendar (
            service_id TEXT PRIMARY KEY,
            monday INTEGER NOT NULL,
            tuesday INTEGER NOT NULL,
            wednesday INTEGER NOT NULL,
            thursday INTEGER NOT NULL,
            friday INTEGER NOT NULL,
            saturday INTEGER NOT NULL,
            sunday INTEGER NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL
        )
    """)


def create_trips_table(cursor: sqlite3.Cursor) -> None:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trips (
            trip_id TEXT PRIMARY KEY,
            route_id TEXT NOT NULL,
            service_id TEXT NOT NULL,
            trip_headsign TEXT,
            direction_id INTEGER,

            FOREIGN KEY (route_id)
                REFERENCES routes(route_id),

            FOREIGN KEY (service_id)
                REFERENCES calendar(service_id)
        )
    """)


def create_stop_times_table(cursor: sqlite3.Cursor) -> None:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stop_times (
            trip_id TEXT NOT NULL,
            arrival_time TEXT NOT NULL,
            departure_time TEXT NOT NULL,
            stop_id TEXT NOT NULL,
            stop_sequence INTEGER NOT NULL,

            PRIMARY KEY (trip_id, stop_sequence),

            FOREIGN KEY (trip_id)
                REFERENCES trips(trip_id),

            FOREIGN KEY (stop_id)
                REFERENCES stops(stop_id)
        )
    """)


#def create_indexes(cursor: sqlite3.Cursor) -> None:
#    cursor.execute("""
#        CREATE INDEX IF NOT EXISTS idx_stop_times_stop
#        ON stop_times(stop_id)
#    """)
#
#    cursor.execute("""
#        CREATE INDEX IF NOT EXISTS idx_stop_times_trip
#        ON stop_times(trip_id)
#    """)
#
#    cursor.execute("""
#        CREATE INDEX IF NOT EXISTS idx_trips_route
#        ON Trips(route_id)
#    """)
#
#    cursor.execute("""
#        CREATE INDEX IF NOT EXISTS idx_trips_service
#        ON Trips(service_id)
#    """)


def create_database(db_path: Path) -> None:
    with sqlite3.connect(db_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        cursor = connection.cursor()

        create_stops_table(cursor)
        create_routes_table(cursor)
        create_calendar_table(cursor)
        create_trips_table(cursor)
        create_stop_times_table(cursor)

        #create_indexes(cursor)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            f"Usage: python {Path(sys.argv[0]).name} <database name>",
            file=sys.stderr
        )
        sys.exit(1)

    try:
        db_path = Path(sys.argv[1]).with_suffix(".sqlite")
        create_database(db_path)

    except PermissionError:
        print(
            f"Permission denied: cannot create database '{sys.argv[1]}'",
            file=sys.stderr
        )
        sys.exit(1)

    except sqlite3.OperationalError as e:
        print(
            f"Database error:\n{e}",
            file=sys.stderr
        )
        sys.exit(1)

    except Exception as e:
        print(
            f"An unexpected error occured:\n{e}",
            file=sys.stderr
        )
        sys.exit(1)