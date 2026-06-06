from pathlib import Path
from Measurements import *


if __name__ == "__main__":
    
    base_path = Path(__file__).parent
    measurements_folder = base_path / "data" / "measurements"
    ms = Measurements(measurements_folder)

    ts = ms.get_by_parameter('PM25')[0]

    print(f'unit: {ts.unit}, value: {ts.values[0]}')
    ts.unit = 'ng/m3'
    print('Set to ng/m3')
    print(f'unit: {ts.unit}, value: {ts.values[0]}')
    ts.unit = 'ug/m3'
    print('Set to ug/m3')
    print(f'unit: {ts.unit}, value: {ts.values[0]}')
    