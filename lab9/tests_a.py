import pytest
from Station import Station  
from datetime import datetime

@pytest.fixture
def create_station():

    def _make_station(station_code: str, **kwargs):
        defaults = {
            'international_code' : 'Random int. code',
            'name' : 'Random name',
            'old_code' : None,
            'launch_date' : datetime(2026, 6, 4),
            'close_date' : None,
            'station_type' : 'Random station type',
            'area_type' : 'Random are type',
            'operational_type' : 'Random operational time',
            'voivodeship' : 'Random voivodeship',
            'city' : 'Random city',
            'address' : 'Random address',
            'north' : 21.,
            'east' : .37
        }
       
        defaults.update(kwargs)
        return Station(code=station_code, **defaults)
    
    return _make_station

@pytest.mark.parametrize(
    'code1, code2, expected_result',
    [
        ('DsJelGorOgin', 'DsJelGorOgin', True),
        ('DsJelGorOgin', 'DsLegAlRzecz', False),
    ]
)

def test_station_comparison(create_station, code1: str, code2: str, expected_result: bool):

    station1 = create_station(code1)
    station2 = create_station(code2)
    
    assert (station1 == station2) is expected_result


def test_station_comparison_with_other_types(create_station):
    
    station = create_station('c-o-d-e')

    assert station != 'DsJelGorOgin'