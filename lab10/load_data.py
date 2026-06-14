import sys
from pathlib import Path
import zipfile
import csv
import io
import sqlite3
from itertools import batched
from typing import Iterator


def load_table_from_zip(
        zip_file: zipfile.ZipFile,
        file_name: str,
        conn: sqlite3.Connection,
        insert_query: str,
        columns_mapping: list[str],
        batch_size: int = 50_000
) -> None:
    with zip_file.open(file_name) as f:
        text_file: io.TextIOWrapper = io.TextIOWrapper(f, encoding='utf-8-sig')
        reader: csv.DictReader[str] = csv.DictReader(text_file)
        data_to_insert: Iterator[tuple[str | None, ...]] = (
            tuple(row.get(col, None) for col in columns_mapping)
            for row in reader
        )
        cursor: sqlite3.Cursor = conn.cursor()
        for batch in batched(data_to_insert, n=batch_size):
            cursor.executemany(insert_query, batch)
            conn.commit()


def load_data(zip_path: Path, db_path: Path) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys = ON")

        with zipfile.ZipFile(zip_path, 'r') as archive:
            load_table_from_zip(
                archive, 'stops.txt', conn,
                "INSERT OR REPLACE INTO stops (stop_id, stop_code, stop_name, stop_lat, stop_lon) VALUES (?, ?, ?, ?, ?)",
                ['stop_id', 'stop_code', 'stop_name', 'stop_lat', 'stop_lon']
            )
            load_table_from_zip(
                archive, 'routes.txt', conn,
                "INSERT OR REPLACE INTO routes (route_id, agency_id, route_short_name, route_long_name, route_desc, route_type) VALUES (?, ?, ?, ?, ?, ?)",
                ['route_id', 'agency_id', 'route_short_name', 'route_long_name', 'route_desc', 'route_type']
            )
            load_table_from_zip(
                archive, 'calendar.txt', conn,
                "INSERT OR REPLACE INTO calendar (service_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                ['service_id', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'start_date', 'end_date']
            )
            load_table_from_zip(
                archive, 'trips.txt', conn,
                "INSERT OR REPLACE INTO trips (trip_id, route_id, service_id, trip_headsign, direction_id) VALUES (?, ?, ?, ?, ?)",
                ['trip_id', 'route_id', 'service_id', 'trip_headsign', 'direction_id']
            )
            load_table_from_zip(
                archive, 'stop_times.txt', conn,
                "INSERT OR REPLACE INTO stop_times (trip_id, arrival_time, departure_time, stop_id, stop_sequence) VALUES (?, ?, ?, ?, ?)",
                ['trip_id', 'arrival_time', 'departure_time', 'stop_id', 'stop_sequence'],
                batch_size=100_000
            )
            


if __name__=='__main__':
    if len(sys.argv) < 3:
        print(f"Usage: python {Path(sys.argv[0]).name} <GTFS_archive.zip> <database_name>")
        exit(1)
    
    zip_path = Path(sys.argv[1])
    db_path = Path(sys.argv[2]).with_suffix('.sqlite')
    load_data(zip_path, db_path)