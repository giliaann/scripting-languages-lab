from dataclasses import dataclass

from typing import List, Optional
from sqlalchemy import ForeignKey, String, Float
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship


@dataclass
class StopStats:
    stop_id: str
    stop_name: str
    line_count: int
    departure_count: int
    earliest_departure: str
    latest_departure: str
    top_directions: list[tuple[str, int]]
    next_n_departures: list[tuple[str, str, str]]


class Base(DeclarativeBase):
    pass

class Stop(Base):
    __tablename__ = "stops"
    
    stop_id: Mapped[str] = mapped_column(String, primary_key=True)
    stop_code: Mapped[Optional[str]]
    stop_name: Mapped[str] = mapped_column(String)
    stop_lat: Mapped[float] = mapped_column(Float)
    stop_lon: Mapped[float] = mapped_column(Float)

    stop_times: Mapped[List["StopTime"]] = relationship(back_populates="stop")

    def __repr__(self) -> str:
        return f"<Stop(stop_id={self.stop_id}, stop_name={self.stop_name})>"


class Route(Base):
    __tablename__ = "routes"
    
    route_id: Mapped[str] = mapped_column(String, primary_key=True)
    agency_id: Mapped[str]
    route_short_name: Mapped[Optional[str]]
    route_long_name: Mapped[Optional[str]]
    route_desc: Mapped[Optional[str]]
    route_type: Mapped[int]

    trips: Mapped[List["Trip"]] = relationship(back_populates="route")


class Calendar(Base):
    __tablename__ = "calendar"
    
    service_id: Mapped[str] = mapped_column(String, primary_key=True)
    monday: Mapped[int]
    tuesday: Mapped[int]
    wednesday: Mapped[int]
    thursday: Mapped[int]
    friday: Mapped[int]
    saturday: Mapped[int]
    sunday: Mapped[int]
    start_date: Mapped[str]
    end_date: Mapped[str]

    trips: Mapped[List["Trip"]] = relationship(back_populates="service")


class Trip(Base):
    __tablename__ = "trips"
    
    trip_id: Mapped[str] = mapped_column(String, primary_key=True)
    route_id: Mapped[str] = mapped_column(ForeignKey("routes.route_id"))
    service_id: Mapped[str] = mapped_column(ForeignKey("calendar.service_id"))
    trip_headsign: Mapped[Optional[str]]
    direction_id: Mapped[Optional[int]]

    route: Mapped["Route"] = relationship(back_populates="trips")
    service: Mapped["Calendar"] = relationship(back_populates="trips")
    stop_times: Mapped[List["StopTime"]] = relationship(back_populates="trip")


class StopTime(Base):
    __tablename__ = "stop_times"
    
    trip_id: Mapped[str] = mapped_column(ForeignKey("trips.trip_id"), primary_key=True)
    stop_sequence: Mapped[int] = mapped_column(primary_key=True)
    
    arrival_time: Mapped[str]
    departure_time: Mapped[str]
    stop_id: Mapped[str] = mapped_column(ForeignKey("stops.stop_id"))

    trip: Mapped["Trip"] = relationship(back_populates="stop_times")
    stop: Mapped["Stop"] = relationship(back_populates="stop_times")