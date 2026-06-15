from dataclasses import dataclass


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