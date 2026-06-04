from TimeSeries import TimeSeries
from SeriesValidator import *
from Measurements import Measurements
from pathlib import Path
from pprint import pprint

class SimpleReporter:
    
    def analyze(self, series: TimeSeries) -> list[str]:
        messages = [f'Info: {series.indicator_name} at {series.station_code} has mean = {series.mean}']
        return messages
    
if __name__ == "__main__":
    
    base_path = Path(__file__).parent.parent
    measurements_folder = base_path / "lab6" / "data" / "measurements"
    ms = Measurements(measurements_folder)

    ts = ms.get_by_parameter('CO')[0]

    series_validators = [ZeroSpikeDetector(), OutlierDetector(5.), ThresholdDetector(2.), SimpleReporter()]

    pprint([validator.analyze(ts) for validator in series_validators])
