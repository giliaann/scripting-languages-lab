import sqlite3
from datetime import datetime
from pathlib import Path

class GTFSDatabase:
    """Class for handling connection with database."""
    
    def __init__(self, db_path: Path) -> None:
        self._conn: sqlite3.Connection = sqlite3.connect(db_path)
        self._conn.execute("PRAGMA foreign_keys = ON")


    def fetch_all_stops(self) -> list[tuple[str, str]]:
        """Returns all stops sorted alphabetically: [(stop_id, stop_name), ...]."""
        query: str = """
            SELECT stop_id, stop_name
            FROM stops
            ORDER BY stop_name
        """
        cursor: sqlite3.Cursor = self._conn.cursor()
        cursor.execute(query)
        return [(str(row[0]), str(row[1])) for row in cursor.fetchall()]
    

    def fetch_stops_query(self, like_reg: str) -> list[tuple[str, str]]:
        """Returns all stops sorted alphabetically and filtered: [(stop_id, stop_name), ...]"""
        query: str = """
            SELECT stop_id, stop_name
            FROM stops
            WHERE stop_name LIKE ?
            ORDER BY stop_name
        """
        cursor: sqlite3.Cursor = self._conn.cursor()
        cursor.execute(query, (f"%{like_reg}%", ))
        return [(str(row[0]), str(row[1])) for row in cursor.fetchall()]
    

    def count_unique_lines_for_stop(self, stop_id: str) -> int:
        """Returns the number of distinct routes serving a stop."""
        query = """
            SELECT COUNT(DISTINCT t.route_id)
            FROM stop_times st
            JOIN trips t ON st.trip_id = t.trip_id
            WHERE st.stop_id = ?
        """
        cursor: sqlite3.Cursor = self._conn.cursor()
        cursor.execute(query, (stop_id, ))
        return int(cursor.fetchone()[0])
    

    def count_departures(self, stop_id: str) -> int:
        """Returns the total number of departures from a stop."""
        query = """
            SELECT COUNT(*)
            FROM stop_times
            WHERE stop_id = ? 
        """
        cursor: sqlite3.Cursor = self._conn.cursor()
        cursor.execute(query, (stop_id, ))
        return int(cursor.fetchone()[0])
    

    def fetch_time_window(self, stop_id: str) -> tuple[str, str]:
        """Returns (earliest, latest) departure time from a stop."""
        query = """
            SELECT MIN(departure_time), MAX(departure_time)
            FROM stop_times
            WHERE stop_id = ?
        """
        cursor: sqlite3.Cursor = self._conn.cursor()
        cursor.execute(query, (stop_id, ))
        min_t, max_t = cursor.fetchone()
        return (min_t if min_t else "None", max_t if max_t else "None")
    

    def fetch_top_directions(self, stop_id: str, max_stops_count: int) -> list[tuple[str, int]]:
        """
        Returns the most common trip headsigns from a stop:
        [(trip_headsign, count), ...].
        """
        query = """
            SELECT t.trip_headsign, COUNT(*) as count
            FROM stop_times st
            JOIN trips t ON st.trip_id = t.trip_id
            WHERE st.stop_id = ?
            GROUP BY t.trip_headsign
            ORDER BY count DESC
            LIMIT ?
        """
        cursor: sqlite3.Cursor = self._conn.cursor()
        cursor.execute(query, (stop_id, max_stops_count))
        return [
            (str(row[0]), int(row[1]))
            for row in cursor.fetchall()
        ]
    

    def fetch_next_n_departures(self, stop_id: str, dt_obj: datetime, n: int) -> list[tuple[str, str, str]]:
        """
        Returns the next n departures from a specific stop based on a given datetime object.
        Returns: [(line_number, direction/headsign, departure_time), ...]
        """
        start_time: str = dt_obj.strftime("%H:%M:%S")
        current_date: str = dt_obj.strftime("%Y%m%d")
        current_day: str = dt_obj.strftime("%A").lower()

        query = f"""
            SELECT r.route_short_name, t.trip_headsign, st.departure_time
            FROM stop_times st
            JOIN trips t ON st.trip_id = t.trip_id
            JOIN routes r ON t.route_id = r.route_id
            JOIN calendar c ON t.service_id = c.service_id
            WHERE st.stop_id = ? 
              AND st.departure_time >= ?
              AND ? BETWEEN c.start_date AND c.end_date
              AND c.{current_day} = 1
            ORDER BY st.departure_time ASC
            LIMIT ?
        """

        cursor: sqlite3.Cursor = self._conn.cursor()
        cursor.execute(query, (stop_id, start_time, current_date, n))
        return [
            (str(row[0]), str(row[1]), str(row[2]))
            for row in cursor.fetchall()
        ]
            
    
