from abc import ABC, abstractmethod
from TimeSeries import TimeSeries
from datetime import datetime

class SeriesValidator(ABC):
    @abstractmethod
    def analyze(self, series: TimeSeries) -> list[str]:
        pass


class OutlierDetector(SeriesValidator):
    def __init__(self, k: float) -> None:
        self.k : float = k

    def analyze(self, series: TimeSeries) -> list[str]:
        avg: float | None = series.mean
        std: float | None = series.stddev

        if avg is None or std is None or std == 0:
            return []
        

        messages: list[str] = [
            f"Outlier: {dt} value {val:.3} exceeds {self.k}*std - {self.k*std:.3}"
            for dt, val in series 
            if val is not None and abs(val - avg) > self.k*std
        ]
        return messages
        


class ZeroSpikeDetector(SeriesValidator):
    def analyze(self, series: TimeSeries) -> list[str]:
        messages: list[str] = []
        count: int = 0
        start_dt: datetime | None = None

        for dt, val in series:
            if val == 0 or val is None:
                if count == 0:
                    start_dt = dt
                count += 1
            else:
                if count >= 3:
                    messages.append(f"Spotted sequence of {count} missing data starting from {start_dt}")
                count = 0
        
        if count >= 3:
            messages.append(f"Spotted sequence of {count} missing data starting from {start_dt}")

        return messages
    

class ThresholdDetector(SeriesValidator):
    def __init__(self, threshold: float) -> None:
        self.threshold: float = threshold


    def analyze(self, series: TimeSeries) -> list[str]:
        messages: list[str] = [
            f"Threshold: {dt} value {val} exceeds threshold {self.threshold}"
            for dt, val in series
            if val is not None and val > self.threshold
        ]
        return messages
        