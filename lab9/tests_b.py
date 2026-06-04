import pytest
import numpy as np
from datetime import datetime, date
from TimeSeries import TimeSeries


@pytest.fixture
def create_time_series():

    def _make_ts(**kwargs):
        default_dates = np.array([
            '2026-06-01T10:15:30', 
            '2026-06-01T11:45:12', 
            '2026-06-02T12:00:05'
        ], dtype='datetime64')
        
        default_values = np.array([12.5, np.nan, 30.0], dtype=np.float64)
        
        defaults = {
            'indicator_name': 'CO',
            'station_code': 'DsJelGorOgin',
            'averaging_time': '1h',
            'dates': default_dates,
            'values': default_values,
            'unit_in': 'mg/m3'
        }
        
        defaults.update(kwargs)
        
        return TimeSeries(**defaults)
        
    return _make_ts


# i
def test_getitem_int_index(create_time_series):
    
    ts = create_time_series()
    
    
    dt1, val1 = ts[0]
    assert dt1 == datetime(2026, 6, 1, 10, 15, 30) 
    assert val1 == 12.5

    dt2, val2 = ts[1]
    assert dt2 == datetime(2026, 6, 1, 11, 45, 12)
    assert val2 is None

# ii
def test_getitem_slice(create_time_series):
    ts = create_time_series()
    
    result = ts[0:2]
    
    expected = [
        (datetime(2026, 6, 1, 10, 15, 30), 12.5),
        (datetime(2026, 6, 1, 11, 45, 12), None)
    ]
    
    assert result == expected
    assert len(result) == 2

# iii
def test_getitem_date_existing(create_time_series):
    ts = create_time_series()
    
    target_date = date(2026, 6, 1)
    
    result = ts[target_date]
    
    assert result == [12.5, None]


# iv
def test_getitem_date_missing(create_time_series):
    ts = create_time_series()
    
    missing_date = date(2026, 6, 15)
    
    with pytest.raises(KeyError) as exc_info:
        _ = ts[missing_date]
        
    assert str(missing_date) in str(exc_info.value)