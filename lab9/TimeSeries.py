from dataclasses import dataclass
from datetime import datetime, date
import numpy as np
import numpy.typing as npt
from collections.abc import Iterator


@dataclass
class TimeSeries:
    indicator_name: str
    station_code: str
    averaging_time: str
    dates: npt.NDArray[np.datetime64]
    values: npt.NDArray[np.float64]
    unit_in: str

    def __post_init__(self) -> None:

        if len(self.dates) != len(self.values):
            raise ValueError(f"Invalid data, length of dates {len(self.dates)} is not equal to length of values {len(self.values)}")


    def __len__(self) -> int:
        return len(self.values)


    def __getitem__(self, key: int | slice | datetime | date) -> tuple[datetime, float | None] | list[tuple[datetime, float | None]] | float | None | list[float | None]:
        match key:
            case int():

                val_i: np.float64 = self.values[key]
                dt: datetime = self.dates[key].item()

                return dt, None if np.isnan(val_i) else float(val_i)
            
            case slice():

                dates: list[datetime] = [d.item() for d in self.dates[key]]
                values_s: list[float | None] = [
                    None if np.isnan(v) else float(v) for v in self.values[key]
                ]

                return list(zip(dates, values_s))
            
            case datetime():

                indices: npt.NDArray[np.intp] = np.where(self.dates == np.datetime64(key))[0]
            
                if indices.size == 0:
                    raise KeyError(f"No datetime key: {key}")
                
                val: np.float64 = self.values[indices[0]]
                return None if np.isnan(val) else float(val)
            
            case date():
                
                dates_only: npt.NDArray[np.datetime64] = self.dates.astype('datetime64[D]')
                dates_mask: npt.NDArray[np.bool_] = dates_only == np.datetime64(key)

                if np.sum(dates_mask) == 0:
                    raise KeyError(f"No datet key: {key}")
                
                values_d: npt.NDArray[np.float64] = self.values[dates_mask]
                
                return [None if np.isnan(v) else float(v) for v in values_d]

            case _:
                raise TypeError(f"Invalid index type: {type(key).__name__}")
    
    @property
    def mean(self) -> float | None:

        if self.values.size == 0 or np.isnan(self.values).all():
            return None

        return float(np.nanmean(self.values))
    

    @property
    def stddev(self) -> float | None:
        
        if self.values.size == 0 or np.isnan(self.values).all():
            return None

        return float(np.nanstd(self.values))
    
    @property
    def unit(self) -> str:
        return self.unit_in
    
    @unit.setter
    def unit(self, new_unit : str) -> None:
        
        if self.unit == 'ng/m3' and new_unit == 'ug/m3':
            self.unit_in = new_unit
            self.values /= 1000.0
        
        elif self.unit == 'ug/m3' and new_unit == 'ng/m3':
            self.unit_in = new_unit
            self.values *= 1000.0
        
        elif new_unit != 'ug/m3' and new_unit != 'ng/m3':
            raise ValueError(f'unit: {new_unit} is not supproted')
        
        return
        
    def __iter__(self) -> Iterator[tuple[datetime, float | None]]:
        self._current_index = 0
        return self

    def __next__(self) -> tuple[datetime, float | None]:
        
        if self._current_index >= len(self):
            raise StopIteration
        
        val = self.values[self._current_index]
        dt = self.dates[self._current_index].item()
        self._current_index += 1
        
        return dt, (None if np.isnan(val) else float(val))
