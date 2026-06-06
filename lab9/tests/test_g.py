import pytest
from Measurements import Measurements
from conftest import MockTimeSeries
from SeriesValidator import OutlierDetector, ZeroSpikeDetector, ThresholdDetector
from ducky_code import SimpleReporter
import numpy as np


@pytest.mark.parametrize(
    "analizers",
    [
        [OutlierDetector(k=2.0), ],
        [ZeroSpikeDetector(), ],
        [ThresholdDetector(threshold=10.0), ],
        [SimpleReporter(), ],
        [OutlierDetector(k=2.0), ZeroSpikeDetector(), ThresholdDetector(threshold=10.0), SimpleReporter()]
    ]
)
def test_detect_all_anomalies(analizers, create_measurements):
    values = np.array([10.5, 999.0, None, 0.0, None, 0.0, 0.0, 0.0, 25.0], dtype=np.float64)
    dates = np.array([f'2026-01-0{i}' for i in range(1, 10)], dtype=np.datetime64)

    ms = create_measurements(values=values, dates=dates)
    result = ms.detect_all_anomalies(analizers, preload=False)
    messages = list(result.values())[0]
    
    assert isinstance(messages, list)
    for msg in messages:
        assert isinstance(msg, str)