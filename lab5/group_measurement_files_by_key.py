from pathlib import Path
import re
from pprint import pprint

'''
This function extracts measurements files (<year>_<measurand>_<frequency>.csv) from the given directory
Output format: 
{
(<year>, <measurand>, <frequency>) : <file_path>
...
}
'''

def group_measurement_files_by_key(path: Path):
    
    result = {}

    for file_path in path.iterdir():
        if not file_path.is_file():
            continue
            
        pattern = re.compile(r"^(\d{4})_([^_]+)_([^.]+)\.csv$")
        if (match := pattern.match(file_path.name)):
            result[match.groups()] = file_path.absolute()

    return result

if __name__ == "__main__":
    pprint(group_measurement_files_by_key(Path('lab5/data/measurements')))