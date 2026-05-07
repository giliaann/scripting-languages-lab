from dataclasses import dataclass
from datetime import datetime


@dataclass
class Measurement:
    date: datetime
    value: float | None
    station: str
    measurement: str


def invalid_values_ratio(measourments: list[Measurement]) -> float:
    return sum(1 for mes in measourments if mes.value is None or mes.value <= 0) / len(measourments) if measourments else 0


def count_big_jumps(measourments: list[Measurement], delta_value_threshold: float) -> int:
    prev = None
    big_jumps = 0

    for measurement in measourments:
        value = measurement.value
        if value is None:
            continue

        if prev is not None:
            if abs(value - prev) > delta_value_threshold:
                big_jumps += 1
        prev = value
    
    return big_jumps


def count_alarmic_values(measurements: list[Measurement], value_threshold: float) -> int:
    return sum(1 for measurement in measurements if measurement.value is not None and measurement.value > value_threshold)


def detect_anomalies(
        measurements: list[Measurement],
        delta_value_threshold: float = 5.0,
        big_jumps_threshold: int = 5,
        invalid_values_ratio_threshold: float = 0.04,
        value_threshold: float = 26.0
) -> list[str]:
    """
    Spots anomalies. 
    Returns list of observed anomalies.
    """
    if not measurements:
        return []
    
    anomalies = []
    measurements = sorted(measurements, key = lambda mes: mes.date)
    
    # za duzy stosunek brakujacych wartosci
    invalid_ratio = invalid_values_ratio(measurements)
    if invalid_ratio > invalid_values_ratio_threshold:
        anomalies.append("Too much invalid values")

    # nagle skoki pomiedzy wartosciami
    big_jumps = count_big_jumps(measurements, delta_value_threshold)
    if big_jumps > big_jumps_threshold:
        anomalies.append(f"Detected {big_jumps} big jumps (>{delta_value_threshold})")

    # wartosci alarmowe
    alarmic_count = count_alarmic_values(measurements, value_threshold)
    if alarmic_count:
        anomalies.append(f"Alarm threshold exceeded {alarmic_count} times (>{value_threshold})")

    return anomalies
