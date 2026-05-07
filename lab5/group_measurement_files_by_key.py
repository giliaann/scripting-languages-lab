from pathlib import Path
import re
import logging
'''
This function extracts measurements files (<year>_<measurand>_<frequency>.csv) from the given directory
Output format: 
{
(<year>, <measurand>, <frequency>) : <file_path>
...
}
'''

def group_measurement_files_by_key(path: Path, log):
    
    result = {}

    if not path.is_dir():
        if log:
            logging.critical(f"{path} is not a directory - measurement files not found!")
        return result

    for file_path in path.iterdir():
        if not file_path.is_file():
            continue
            
        pattern = re.compile(r"^(\d{4})_([^_]+)_([^.]+)\.csv$")
        if (match := pattern.match(file_path.name)):
            result[match.groups()] = file_path

    return result

if __name__ == "__main__":
    print(group_measurement_files_by_key(Path('lab5/data/measurements'), False))