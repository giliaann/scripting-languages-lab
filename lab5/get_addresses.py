from utils import parse_metadata_file
from pathlib import Path
import re


'''
This function filters station metadata, leaves only data for a given city and extract addresses
Output format: [(<voivodeship>, <city>, <street>, <number> (if any)), ... ]
'''

def get_addresses(path: Path, city: str):
    data = parse_metadata_file(path)
    pattern = re.compile(r'^(.*?)(?:\s+(\d+\S*))?$')
    result = []

    for _, station_data in data.items():
        if((locality:=station_data['locality']) == city.strip()):
            voivodeship = station_data['voivodeship']
            street = station_data['address']
            number = None
            if(match:=pattern.match(station_data['address'])):
                street = match.group(1).strip()
                if match.group(2):
                    number = match.group(2).strip()
            result.append((voivodeship, locality, street, number))
    
    return result


if __name__ == "__main__":
    print(get_addresses(Path('lab5/data/stacje.csv'), 'Szczecin'))


