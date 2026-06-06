import pytest
from SeriesValidator import ZeroSpikeDetector
from conftest import MockTimeSeries



@pytest.mark.parametrize(
    "data, expected_messages",
    [
        # no zeros or nans => empty list
        (
            [("2026-01-01", 10.5), ("2026-01-02", 12.0), ("2026-01-03", 5.0)],
            []
        ),
        #too short series => empty list
        (
            [("2026-01-01", 0), ("2026-01-02", 0), ("2026-01-03", 15.0)],
            []
        ),
        # anomaly
        (
            [
                ("2026-01-01", 10.0),
                ("2026-01-02", 0),
                ("2026-01-03", None),
                ("2026-01-04", 0),
                ("2026-01-05", 12.5)
            ],
            [
                "Spotted sequence of 3 missing data starting from 2026-01-02",
            ]
        ),
        # anomaly on the end
        (
            [
                ("2026-01-01", 5.0),
                ("2026-02-02", 0),
                ("2026-03-03", 0),
                ("2026-04-04", None),
                ("2026-05-05", None)
            ],
            [
                "Spotted sequence of 4 missing data starting from 2026-02-02"
            ]
        ),
        # two anomalies
        (
            [
                ("2026-07-01", 0), ("2026-07-02", 0), ("2026-07-03", 0),
                ("2026-07-04", 100.0),
                ("2026-07-05", None), ("2026-07-06", 0), ("2026-07-07", 0)
            ],
            [
                "Spotted sequence of 3 missing data starting from 2026-07-01",
                "Spotted sequence of 3 missing data starting from 2026-07-05"
            ]
        )
    ]
)
def test_zero_spike_detector(data, expected_messages):
    mock_series = MockTimeSeries(None, None, data)
    detector = ZeroSpikeDetector()
    results = detector.analyze(mock_series)
    assert results == expected_messages