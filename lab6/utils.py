import csv
import numpy as np
from datetime import datetime
from pathlib import Path
from TimeSeries import TimeSeries


def parse_measurement_file(file_path: str | Path) -> list[TimeSeries]:
    """
    Parses measurment file. Retuns list of TimeSeries.
    """
    
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with path.open(mode='r', encoding='utf-8-sig') as csvfile:
        reader = list(csv.reader(csvfile, delimiter=','))
        
        if len(reader) < 7:
            raise ValueError(f"File {path.name} is invalid - not enough lines.")

        station_codes = [s.strip() for s in reader[1][1:] if s.strip()]
        indicators = reader[2][1:]
        averaging_times = reader[3][1:]
        units = reader[4][1:]
        
        num_stations = len(station_codes)
        
        dates = []
        all_values = [[] for _ in range(num_stations)]

        
        for row in reader[6:]:
            if not row or not row[0].strip(): 
                continue
            
            try:
               
                date_obj = datetime.strptime(row[0].strip(), '%d/%m/%y %H:%M')
                dates.append(date_obj)

            except ValueError:
                continue

            for i in range(num_stations):
               
                if i + 1 < len(row):
                    val_str = row[i + 1].strip().replace(',', '.')
                    if val_str == '':
                        all_values[i].append(None)
                    else:
                        try:
                            all_values[i].append(float(val_str))
                        except ValueError:
                            all_values[i].append(None)
                else:
                    all_values[i].append(None)

        results = []
        for i in range(num_stations):
            ts = TimeSeries(
                indicator_name=indicators[i].strip(),
                station_code=station_codes[i],
                averaging_time=averaging_times[i].strip(),
                dates=dates,
                values=np.array(all_values[i], dtype=float),
                unit_in=units[i].strip()
            )
            results.append(ts)
            
        return results
