from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from sqlalchemy import select, func, distinct, create_engine
from sqlalchemy.orm import Session

from src.models import Stop, Route, Calendar, Trip, StopTime

class GTFSDatabaseORM:
    """Class for handling connection with database using SQLAlchemy."""
    
    def __init__(self, db_path: Path) -> None:
    
        self._engine = create_engine(
            f"sqlite:///{db_path.as_posix()}"
        )
        with self._engine.connect() as conn:
            conn.exec_driver_sql("PRAGMA foreign_keys = ON")
            
        self._session = Session(self._engine)

    def fetch_all_stops(self) -> List[Tuple[str, str]]:
        """Returns all stops sorted alphabetically: [(stop_id, stop_name), ...]."""
        stmt = (
            select(Stop.stop_id, Stop.stop_name)
            .order_by(Stop.stop_name)
        )
        
        results = self._session.execute(stmt).all()
        return [(str(row.stop_id), str(row.stop_name)) for row in results]
    

    def fetch_stops_query(self, like_reg: str) -> List[Tuple[str, str]]:
        """Returns all stops sorted alphabetically and filtered: [(stop_id, stop_name), ...]"""
        stmt = (
            select(Stop.stop_id, Stop.stop_name)
            .where(Stop.stop_name.like(f"%{like_reg}%"))
            .order_by(Stop.stop_name)
        )
        results = self._session.execute(stmt).all()
        return [(str(row.stop_id), str(row.stop_name)) for row in results]
    

    def count_unique_lines_for_stop(self, stop_id: str) -> int:
        """Returns the number of distinct routes serving a stop."""
        stmt = (
            select(func.count(distinct(Trip.route_id)))
            .select_from(StopTime)
            .join(Trip, StopTime.trip_id == Trip.trip_id)
            .where(StopTime.stop_id == stop_id)
        )
        result = self._session.scalar(stmt)
        return int(result) if result else 0
    

    def count_departures(self, stop_id: str) -> int:
        """Returns the total number of departures from a stop."""
        stmt = (
            select(func.count())
            .select_from(StopTime)
            .where(StopTime.stop_id == stop_id)
        )
        result = self._session.scalar(stmt)
        return int(result) if result else 0
    

    def fetch_time_window(self, stop_id: str) -> Tuple[str, str]:
        """Returns (earliest, latest) departure time from a stop."""
        stmt = (
            select(func.min(StopTime.departure_time), func.max(StopTime.departure_time))
            .where(StopTime.stop_id == stop_id)
        )
        row = self._session.execute(stmt).first()
        
        if row and row[0] is not None and row[1] is not None:
            return (str(row[0]), str(row[1]))
        return ("None", "None")
    

    def fetch_top_directions(self, stop_id: str, max_stops_count: int) -> List[Tuple[str, int]]:
        """Returns the most common trip headsigns from a stop."""
        stmt = (
            select(Trip.trip_headsign, func.count().label("count"))
            .select_from(StopTime)
            .join(Trip, StopTime.trip_id == Trip.trip_id)
            .where(StopTime.stop_id == stop_id)
            .group_by(Trip.trip_headsign)
            .order_by(func.count().desc())
            .limit(max_stops_count)
        )
        results = self._session.execute(stmt).all()
        return [(str(row.trip_headsign), int(row.count)) for row in results]
    

    def fetch_next_n_departures(self, stop_id: str, dt_obj: datetime, n: int) -> List[Tuple[str, str, str]]:
        """Returns the next n departures from a specific stop based on a given datetime object."""
        start_time: str = dt_obj.strftime("%H:%M:%S")
        current_date: str = dt_obj.strftime("%Y%m%d")
        current_day: str = dt_obj.strftime("%A").lower()

        day_column = getattr(Calendar, current_day)

        stmt = (
            select(Route.route_short_name, Trip.trip_headsign, StopTime.departure_time)
            .select_from(StopTime)
            .join(Trip, StopTime.trip_id == Trip.trip_id)
            .join(Route, Trip.route_id == Route.route_id)
            .join(Calendar, Trip.service_id == Calendar.service_id)
            .where(
                StopTime.stop_id == stop_id,
                StopTime.departure_time >= start_time,
                Calendar.start_date <= current_date,
                Calendar.end_date >= current_date,
                day_column == 1
            )
            .order_by(StopTime.departure_time.asc())
            .limit(n)
        )
        
        results = self._session.execute(stmt).all()
        return [(str(row.route_short_name), str(row.trip_headsign), str(row.departure_time)) for row in results]
    
    def __del__(self):
        if hasattr(self, '_session'):
            self._session.close()