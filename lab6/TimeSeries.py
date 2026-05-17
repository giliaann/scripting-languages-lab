from dataclasses import dataclass
from datetime import datetime, date
import numpy as np
import numpy.typing as npt


@dataclass
class TimeSeries:
    indicator_name: str
    station_code: str
    averaging_time: str
    dates: list[datetime]
    values: npt.NDAarray[float | None]
    unit_in: str

    def __post_init__(self):
        if not isinstance(self.dates, np.ndarray):
            self.dates = np.array(self.dates)
        if not isinstance(self.values, np.ndarray):
            self.values = np.array(self.values)
        if len(self.dates) != len(self.values):
            raise ValueError(f"Invalid data, length of dates {len(self.dates)} is not equal to length of values {len(self.values)}")

    
    def __len__(self):
        return min(len(self.dates), len(self.values))


    def __getitem__(self, key: int | slice | datetime | date):
        match key:
            case int():
                return self.dates[key], self.values[key]
            case slice():
                return list(zip(self.dates[key], self.values[key]))
            case datetime():
                try:
                    idx = self.dates.index(key)
                    return self.values[idx]
                except ValueError:
                    raise KeyError(f"No datetie key: {key}")
            case date():
                result = [
                    val for d, val in zip(self.dates, self.values)
                    if d is not None and d.date() == key
                ]
                if not result:
                    raise KeyError(f"No date key: {key}")
                return result
            case _:
                raise TypeError(f"Invalid index type: {type(key).__name__}")
    

    def __numeric_values(self):
        valid_data = self.values[self.values != None]
        return valid_data.astype(float)
    

    @property
    def mean(self) -> float | None:
        data = self.__numeric_values()
        return float(np.mean(data)) if data.size != 0 else None
    

    @property
    def stddev(self) -> float | None:
        data = self.__numeric_values()
        return float(np.std(data)) if data.size != 0 else None
    
    @property
    def unit(self) -> str | None:
        return self.unit_in
    
    @unit.setter
    def unit(self, new_unit):
        
        if self.unit == 'ng/m3' and new_unit == 'ug/m3':
            self.unit_in = new_unit
            self.values *= 1000.0
        
        elif self.unit == 'ug/m3' and new_unit == 'ng/m3':
            self.unit_in = new_unit
            self.values /= 1000.0
        
        elif new_unit != 'ug/m3' and new_unit != 'ng/m3':
            raise ValueError(f'unit: {new_unit} is not supproted')
        
        return


