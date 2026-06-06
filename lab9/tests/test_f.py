import pytest
from SeriesValidator import ThresholdDetector
from conftest import MockTimeSeries


@pytest.mark.parametrize(
    "threshold, data, expected_messages",
    [
        # normal anomalies => 2 messages
        (
            15.0,
            [
                ("2026-01-01", 10.0),
                ("2026-01-02", 20.0),
                ("2026-01-03", 15.0),
                ("2026-01-04", 15.00001)
            ],
            [
                "Threshold: 2026-01-02 value 20.0 exceeds threshold 15.0",
                "Threshold: 2026-01-04 value 15.00001 exceeds threshold 15.0",
            ]
        ),
        # no anomalies
        (
            21.5,
            [
                ("2026-01-01", 10.0),
                ("2026-01-02", 20.0),
                ("2026-01-03", 15.0),
                ("2026-01-04", 15.00001)
            ],
            []
        ),
        # empty data
        (
            0.0,
            [],
            []
        ),
        # nans
        (
            -1.0,
            [
                ("2026-01-01", None),
                ("2026-01-02", 0.0),
                ('2026-01-03', -3.0),
                ("2026-01-04", None)
            ],
            [
                "Threshold: 2026-01-02 value 0.0 exceeds threshold -1.0",
            ]
        )
    ]
)
def test_threshold_detector(threshold, data, expected_messages):
    mock_series = MockTimeSeries(None, None, data)
    detector = ThresholdDetector(threshold)
    results = detector.analyze(mock_series)
    assert results == expected_messages