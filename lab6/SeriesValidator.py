from abc import ABC, abstractmethod
from TimeSeries import TimeSeries


class SeriesValidator(ABC):
    @abstractmethod
    def analyze(self, series: TimeSeries) -> list[str]:
        pass


class OutlierDetector(SeriesValidator):
    def __init__(self, k: float):
        self.k = k

    def analyze(self, series: TimeSeries) -> list[str]:
        avg = series.mean
        std = series.stddev

        if avg is None or std is None or std == 0:
            return []
        
        messages = []
        for dt, val in series:
            if val is not None:
                if abs(val - avg) > self.k * std:
                    messages.append(f"Outlier: {dt} value {val} exceeds {self.k}*std")

        messages = [
            f"Outlier: {dt} value {val} exceeds {self.k}*std"
            for dt, val in series 
            if val is not None and abs(val - avg) > self.k*std
        ]
        return messages
        


class ZeroSpikeDetector(SeriesValidator):
    def analyze(self, series: TimeSeries) -> list[str]:
        messages = []
        count = 0
        start_dt = None

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
    def __init__(self, threshold: float):
        self.threshold = threshold


    def analyze(self, series: TimeSeries) -> list[str]:
        messages = [
            f"Threshold: {dt} value {val} exceeds threshold {self.threshold}"
            for dt, val in series
            if val is not None and val > self.threshold
        ]
        return messages
        