import csv
import re
from pathlib import Path
from typing import List, Dict, Set, Union
from TimeSeries import TimeSeries
from SeriesValidator import *
from utils import parse_measurement_file

class Measurements:
    def __init__(self, directory_path: Union[str, Path]):
        
        self.directory_path = Path(directory_path)
        
        self._files_metadata: Dict[Path, Dict] = {}
        self._station_to_files: Dict[str, Set[Path]] = {}
        self._file_to_ts_count: Dict[Path, int] = {}
        self._cache: Dict[Path, List[TimeSeries]] = {}

        self._identify_files_by_name()

    def _identify_files_by_name(self):
        if not self.directory_path.is_dir():
            raise FileNotFoundError(f"{self.directory_path} is not a directory")

        pattern = re.compile(r"(\d{4})_(.*?)_(.*?)\.csv")
        
        for file_path in self.directory_path.iterdir():
            if file_path.is_file() and file_path.suffix == '.csv':
                match = pattern.match(file_path.name)
                if match:
                    self._files_metadata[file_path] = {
                        'year': match.group(1),
                        'parameter': match.group(2),
                        'freq': match.group(3)
                    }

    def _build_station_registry(self):
        '''Reads only first two lines in all files. Checks which stations are included and count them for each file'''
        if self._station_to_files and self._file_to_ts_count:
            return
            
        for path in self._files_metadata:

            with path.open(mode='r', encoding='utf-8-sig') as f:
                
                reader = csv.reader(f)
                try:
                    #skip ids
                    next(reader)

                    stations_codes_line = next(reader)[1:]
                    stations_codes = [s.strip() for s in stations_codes_line if s.strip()]
                    
                    self._file_to_ts_count[path] = len(stations_codes)
                    for s in stations_codes:
                        if s not in self._station_to_files:
                            self._station_to_files[s] = set()
                        self._station_to_files[s].add(path)

                except StopIteration:
                    continue
                    
        self._is_indexed = True

    def _get_ts(self, path: Path) -> List[TimeSeries]:
        '''Reads data from TimeSeries cache or reads it into cache and returns it.'''
        if path in self._cache:
            return self._cache[path]

        series_in_file = parse_measurement_file(path)
        
        self._cache[path] = series_in_file
        return series_in_file

    def __len__(self) -> int:
        '''Returns number of TimeSeries from all measurements files'''
        self._build_station_registry()
        return sum(self._file_to_ts_count.values())

    def __contains__(self, param_name: str) -> bool:
        '''Checks if any station measures given measurement'''
        return any(meta['parameter'] == param_name 
                   for meta in self._files_metadata.values())

    def get_by_parameter(self, param_name: str) -> List[TimeSeries]:
        '''Returns list of all TimeSeries refering to given measurand'''
        results = []
        for path, meta in self._files_metadata.items():
            if meta['parameter'] == param_name:
                results.extend(self._get_ts(path))
        return results

    def get_by_station(self, station_code: str) -> List[TimeSeries]:
        '''Returns list of all TimeSeries measured by a station with given code'''
        self._build_station_registry()
        results = []
        if station_code in self._station_to_files:
            for path in self._station_to_files[station_code]:
                all_ts = self._get_ts(path)
                results.extend([ts for ts in all_ts if ts.station_code == station_code])
        return results
    
    def detect_all_anomalies(self, validators: list[SeriesValidator], preload: bool = False):
        '''Returns list of (ts_brief, anomaly_msg list). 
        If preload is set to True, TimeSeries for all files are analyzed. Otherwise only cache is analyzed'''
        anomalies_messages = []

        ts_lists = [self._get_ts(path) for path in self._files_metadata] if preload else self._cache.values()

        for sub_list in ts_lists:
            for ts in sub_list:
                msg_list = []
                for validator in validators:
    
                    if msg:= validator.analyze(ts):
                        msg_list.extend(msg)

                if msg_list:
                    ts_brief = (
                        ts.indicator_name, 
                        ts.station_code, 
                        ts.averaging_time, 
                        min(ts.dates) if len(ts.dates) else None, 
                        max(ts.dates) if len(ts.dates) else None
                        )
                    anomalies_messages.append((ts_brief, msg_list))

        return anomalies_messages
            
    
if __name__ == "__main__":
    base_path = Path(__file__).parent
    measurements_folder = base_path / "data" / "measurements"
    ms = Measurements(measurements_folder)
    
    assert('CO' in ms)
    assert('PYTHON' not in ms)

    measurand = 'CO'
    print(f'TimeSeries for {measurand} measurand')
    print([f'| {x.indicator_name}, {x.station_code}, {x.mean:.2} {x.unit} |' for x in ms.get_by_parameter(measurand)[:5]])
    print('-'*20)
    code = 'DsJelGorOgin'
    print(f'TimeSeries for station "{code}"')
    print([f'| {x.indicator_name}, {x.station_code}, {x.mean:.2} {x.unit} |' for x in ms.get_by_station(code)[:5]])
    print('-'*20)
    series_validators = [ZeroSpikeDetector(), OutlierDetector(5.), ThresholdDetector(90.)]
    n = 3
    m = 5
    print(f'First {n} detected anomalies for {m} TimeSeries:')
    anomalies = [(brief, msg[:n]) for brief, msg in ms.detect_all_anomalies(series_validators, True)[:m]]
    for x in anomalies:
        print(x)
        print('-'*10)
    