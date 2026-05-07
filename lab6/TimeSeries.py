from dataclasses import dataclass
from datetime import datetime, date
import numpy as np


@dataclass
class TimeSeries:
    indicator_name: str
    station_code: str
    averaging_time: str
    dates: list[datetime]
    values: np.ndarray[float | None]
    unit: str

    def __post_init__(self):
        if not isinstance(self.values, np.ndarray):
            self.values = np.array(self.values)

    
    def __len__(self):
        return len(min(self.dates, self.values))


    def __getitem__(self, key):
        if isinstance(key, (int, slice)):
            result_dates = self.dates[key]
            result_values = self.values[key]
            if isinstance(key, int):
                return (result_dates, result_values)
            return list(zip(result_dates, result_values))
        
        if isinstance(key, (datetime, date)):
            indices = [
                i for i, d in enumerate(self.dates)
                if d == key or (not isinstance(key, datetime) and d.date() == key)
            ]
            if not indices:
                raise KeyError
            results = self.values[indices].tolist()
            return results[0] if len(results) == 1 else results
        raise TypeError(f"Invalid index type: {type(key).__name__}")
    

    @property
    def __numeric_values(self):
        valid_data = self.values[self.values != None]
        return valid_data.astype(float)
    

    @property
    def mean(self) -> float | None:
        data = self.__numeric_values
        return float(np.mean(data)) if data.size != 0 else None
    

    @property
    def stddev(self) -> float | None:
        data = self.__numeric_values
        return float(np.std(data)) if data.size != 0 else None