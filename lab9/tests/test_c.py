import pytest
import numpy as np

@pytest.mark.parametrize(
        "dates, values, expected_output", 
        [
            (
                np.array([f'2026-06-0{i}' for i in range(1,7)], dtype=np.datetime64),
                np.array([10.0, 12.0, 15.5, 12.97, 0.98, 0.00], dtype=np.float64),
                8.575
            ),
            (
                np.array([f'2026-06-0{i}' for i in range(1,6)], dtype=np.datetime64),
                np.array([0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float64),
                0.0
            ),
            (
                np.array([], dtype=np.datetime64),
                np.array([], dtype=np.float64),
                None
            ),
            (
                np.array([f'2026-06-01'], dtype=np.datetime64),
                np.array([2.0], dtype=np.float64),
                2.0
            ),
            (
                np.array([f'2026-06-0{i}' for i in range(1,4)], dtype=np.datetime64),
                np.array([0.25, 0.25, 0.5], dtype=np.float64),
                1/3
            ),
        ]
)
def test_mean_timeseries_without_nans(create_time_series, dates: np.ndarray[np.datetime64], values: np.ndarray[np.float64], expected_output: float | None):
    ts = create_time_series(dates = dates, values = values)

    if expected_output is None:
        assert ts.mean is None
    else:
        assert ts.mean == pytest.approx(expected_output)



@pytest.mark.parametrize(
    "dates, values, expected_output",
    [
        (
            np.array([f'2026-07-1{i}' for i in range(1,7)], dtype=np.datetime64),
            np.array([10.0, 12.0, 15.5, None, None, 0.00], dtype=np.float64),
            9.375
        ),
        (
            np.array([f'2026-07-1{i}' for i in range(1,6)], dtype=np.datetime64),
            np.array([0.0, 0.0, None, None, 0.0], dtype=np.float64),
            0.0
        ),
        (
            np.array([f'2026-07-1{i}' for i in range(1,7)], dtype=np.datetime64),
            np.array([None, None, None, None, None, None], dtype=np.float64),
            None
        ),
        (
            np.array(['2027-01-01'], dtype=np.datetime64),
            np.array([None], dtype=np.float64),
            None
        ),
        (
            np.array([f'2026-07-1{i}' for i in range(1,7)], dtype=np.datetime64),
            np.array([10.0, 12.123, 15.5, None, 1.0, 50.00], dtype=np.float64),
            17.7246
        ),
    ]
)
def test_mean_timeseries_with_nans(create_time_series, dates: np.ndarray[np.datetime64], values: np.ndarray[np.float64], expected_output: float | None):
    ts = create_time_series(dates = dates, values = values)

    if expected_output is None:
        assert ts.mean is None
    else:
        assert ts.mean == pytest.approx(expected_output)


