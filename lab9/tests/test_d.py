import pytest
import numpy as np
from SeriesValidator import OutlierDetector
from conftest import MockTimeSeries


@pytest.mark.parametrize(
    "mean, std, data, k, expected_messages",
    [
        # mean == None => no results
        (None, 2.0, [("2026-01-01", 10.0)], 2.0, []),
        # std == None => no results
        (10.0, None, [("2026-01-01", 10.0)], 2.0, []),
        # std == 0 => no results
        (10.0, 0.0, [("2026-01-01", 10.0)], 2.0, []),
        # no anomalies
        (10.0, 2.0, [
            ("2026-01-01", 10.0),
            ("2026-01-02", 14.0)
        ], 2.0, []),
        # anomalies
        (10.0, 2.0, [
            ("2026-01-01", 10.0),
            ("2026-01-02", 15.0),
            ("2026-01-03", 5.0),
            ("2026-01-04", None)
        ], 2.0, [
            "Outlier: 2026-01-02 value 15.0 exceeds 2.0*std - 4.0",
            "Outlier: 2026-01-03 value 5.0 exceeds 2.0*std - 4.0"
        ]),
    ]
)
def test_outlier_detector(mean, std, data, k, expected_messages):
    mock_series = MockTimeSeries(mean, std, data)
    detector = OutlierDetector(k)
    results = detector.analyze(mock_series)
    assert results == expected_messages