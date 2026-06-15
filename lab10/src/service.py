from datetime import datetime
from src.database import GTFSDatabase
from src.models import StopStats


class TransitService:

    def __init__(self, db: GTFSDatabase) -> None:
        self._db = db

    def search_stops(self, query: str) -> list[tuple[str, str]]:
        """Return stops whose name contains *query*"""
        stops = self._db.fetch_all_stops()
        if not query:
            return stops
        q = query.casefold()
        return [
            (sid, name)
            for sid, name in stops
            if q in name.casefold()
        ]
    

    def get_stop_stats(self, stop_id: str, stop_name: str) -> StopStats:
        """Return all stats for one stop"""
        line_count = self._db.count_unique_lines_for_stop(stop_id)
        departure_count=self._db.count_departures(stop_id)
        departure_window = self._db.fetch_time_window(stop_id)
        top_directions = self._db.fetch_top_directions(stop_id, 4)
        now = datetime.now()
        fake_current_time = datetime(2026, 5, 28, now.hour, now.minute, now.second)
        next_departures = self._db.fetch_next_n_departures(stop_id, fake_current_time, 5)
        return StopStats(
            stop_id=stop_id,
            stop_name=stop_name,
            line_count=line_count,
            departure_count=departure_count,
            earliest_departure=departure_window[0],
            latest_departure=departure_window[1],
            top_directions=top_directions,
            next_n_departures=next_departures
        )
    