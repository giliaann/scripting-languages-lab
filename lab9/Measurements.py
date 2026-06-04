import csv
import re
from pathlib import Path
from TimeSeries import TimeSeries
from SeriesValidator import *
from utils import parse_measurement_file
from collections import defaultdict
from collections.abc import Iterator
from datetime import datetime


class Measurements:
    def __init__(self, directory_path: str | Path) -> None:
        
        self.directory_path = Path(directory_path)
        
        self._files_metadata: dict[Path, dict[str, str]] = {}
        self._station_to_files: dict[str, set[Path]] = defaultdict(set)
        self._file_to_ts_count: dict[Path, int] = {}
        self._cache: dict[Path, list[TimeSeries]] = {}

        self._identify_files_by_name()

    def _identify_files_by_name(self) -> None:
        '''Adds files metadata to dictionary in a format: file_path : {year: str, parameter: str, freq: str}'''
        if not self.directory_path.is_dir():
            raise FileNotFoundError(f"{self.directory_path} is not a directory")

        pattern: re.Pattern[str] = re.compile(r"(\d{4})_(.*)_(.*?)\.csv")
        
        for file_path in self.directory_path.iterdir():
            if file_path.is_file() and file_path.suffix == '.csv':
                match: re.Match[str] | None = pattern.match(file_path.name)
                if match:
                    self._files_metadata[file_path] = {
                        'year': match.group(1),
                        'parameter': match.group(2),
                        'freq': match.group(3)
                    }

    def _build_station_registry(self) -> None:
        '''Reads only first two lines in all files. Checks which stations are included and count them for each file'''
        if self._station_to_files and self._file_to_ts_count:
            return
            
        for path in self._files_metadata:

            with path.open(mode='r', encoding='utf-8-sig') as f:
                
                reader: Iterator[list[str]] = csv.reader(f)
                try:
                    #skip ids
                    next(reader)

                    stations_codes_line: list[str] = next(reader)[1:]
                    stations_codes: list[str] = [s.strip() for s in stations_codes_line if s.strip()]
                    
                    self._file_to_ts_count[path] = len(stations_codes)
                    for s in stations_codes:
                        self._station_to_files[s].add(path)

                except StopIteration:
                    continue

    def _get_ts(self, path: Path) -> list[TimeSeries]:
        '''Reads data from TimeSeries cache or reads it into cache and returns it.'''
        if path in self._cache:
            return self._cache[path]

        series_in_file: list[TimeSeries] = parse_measurement_file(path)
        
        self._cache[path] = series_in_file
        return series_in_file

    def __len__(self) -> int:
        '''Returns number of TimeSeries from all measurements files'''
        self._build_station_registry()
        return sum(self._file_to_ts_count.values())

    def __contains__(self, param_name: str) -> bool:
        '''Checks if any station measures given measurement'''
        self._build_station_registry()
        return any(
            meta['parameter'] == param_name
            for path, meta in self._files_metadata.items()
            if self._file_to_ts_count[path] > 0
        )

    def get_by_parameter(self, param_name: str) -> list[TimeSeries]:
        '''Returns list of all TimeSeries refering to given measurand'''
        results: list[TimeSeries] = []
        for path, meta in self._files_metadata.items():
            if meta['parameter'] == param_name:
                results.extend(self._get_ts(path))
        return results

    def get_by_station(self, station_code: str) -> list[TimeSeries]:
        '''Returns list of all TimeSeries measured by a station with given code'''
        self._build_station_registry()
        results: list[TimeSeries] = []
        if station_code in self._station_to_files:
            for path in self._station_to_files[station_code]:
                all_ts: list[TimeSeries] = self._get_ts(path)
                results.extend([ts for ts in all_ts if ts.station_code == station_code])
        return results
    
    def detect_all_anomalies(self, validators: list[SeriesValidator], preload: bool = False) -> dict[tuple[str, str, str, datetime, datetime], list[str]]:
        '''
        Returns dict TimeSeries_brief : anomalies_list. 
        If preload is set to True, TimeSeries for all files are analyzed. Otherwise only cache is analyzed
        '''
        
        ts_to_anomalies: dict[tuple[str, str, str, datetime, datetime], list[str]] = {}

        ts_lists = [self._get_ts(path) for path in self._files_metadata] if preload else self._cache.values()

        for sub_list in ts_lists:
            for ts in sub_list:
                msg_list: list[str] = []
                for validator in validators:
                    if msg := validator.analyze(ts):
                        msg_list.extend(msg)

                if msg_list:

                    ts_brief: tuple[str, str, str, datetime, datetime] = (
                        ts.indicator_name, 
                        ts.station_code, 
                        ts.averaging_time, 
                        min(ts.dates).item(), 
                        max(ts.dates).item()
                        )
                    ts_to_anomalies[ts_brief] = msg_list

        return ts_to_anomalies
            
    
if __name__ == "__main__":
    base_path = Path(__file__).parent.parent
    measurements_folder = base_path / "lab6" / "data" / "measurements"
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
    ts_to_anomalies = ms.detect_all_anomalies(series_validators, False)
    
    print(f'First {n} detected anomalies for {m} TimeSeries:')
    for ts, anomalies in ts_to_anomalies.items():
        print(ts, anomalies[:n])
        print('-'*10)
        
        m-=1
        if m<= 0: 
            break
    