import pytest
import numpy as np
from TimeSeries import TimeSeries
from Station import Station
from datetime import datetime
from Measurements import Measurements


class MockTimeSeries:
    def __init__(self, mean: float | None, stddev: float | None, data: list):
        self.mean = mean
        self.stddev = stddev
        self.data = data


    def __iter__(self):
        return iter(self.data)


@pytest.fixture
def create_station():

    def _make_station(station_code: str, **kwargs):
        defaults = {
            "international_code": "Random int. code",
            "name": "Random name",
            "old_code": None,
            "launch_date": datetime(2026, 6, 4),
            "close_date": None,
            "station_type": "Random station type",
            "area_type": "Random are type",
            "operational_type": "Random operational time",
            "voivodeship": "Random voivodeship",
            "city": "Random city",
            "address": "Random address",
            "north": 21.0,
            "east": 0.37,
        }

        defaults.update(kwargs)
        return Station(code=station_code, **defaults)

    return _make_station


@pytest.fixture
def create_time_series():

    def _make_ts(**kwargs):
        default_dates = np.array(
            ["2026-06-01T10:15:30", "2026-06-01T11:45:12", "2026-06-02T12:00:05"], dtype="datetime64"
        )

        default_values = np.array([12.5, np.nan, 30.0], dtype=np.float64)

        defaults = {
            "indicator_name": "CO",
            "station_code": "DsJelGorOgin",
            "averaging_time": "1h",
            "dates": default_dates,
            "values": default_values,
            "unit_in": "mg/m3",
        }

        defaults.update(kwargs)

        return TimeSeries(**defaults)

    return _make_ts


@pytest.fixture
def create_measurements(tmp_path, create_time_series):

    def _make_measurements(**kwargs):
        ms = Measurements(tmp_path)
        mock_ts = create_time_series(**kwargs)
        dummy_file_path = tmp_path / "2026_CO_1h.csv"
        ms._cache[dummy_file_path] = [mock_ts]

        return ms
    
    return _make_measurements


