import pytest
from Station import Station
from datetime import datetime


@pytest.mark.parametrize(
    "code1, code2, expected_result",
    [
        ("DsJelGorOgin", "DsJelGorOgin", True),
        ("DsJelGorOgin", "DsLegAlRzecz", False),
    ],
)
def test_station_comparison(create_station, code1: str, code2: str, expected_result: bool):

    station1 = create_station(code1)
    station2 = create_station(code2)

    assert (station1 == station2) is expected_result


def test_station_comparison_with_other_types(create_station):

    station = create_station("c-o-d-e")

    assert station != "DsJelGorOgin"
