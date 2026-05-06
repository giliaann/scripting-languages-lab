from utils import parse_metadata_file, pl_latin_char_map
from pathlib import Path
import re


'''
a) This functions reads all dates from metadata file and returns them in a list
'''
def extract_dates(path: Path):
    
    data = parse_metadata_file(path)
    pattern = re.compile(r'\b\d{4}-\d{2}-\d{2}\b')
    
    result = []

    for _, station_data in data.items():
        for date_key in ['launch_date', 'close_date']:
            if(match := pattern.match(station_data[date_key])):
                result.append(match.group(0))

    return result

'''
b) This functions reads all coordinates from metadata file and returns them in a list
'''
def extract_coords(path: Path):
    
    data = parse_metadata_file(path)
    pattern = re.compile(r'-?\d+\.\d{6}\b')
    
    result = []

    for _, station_data in data.items():
        for coord_key in ['WGS84N', 'WGS84E']:
            if(match := pattern.match(station_data[coord_key])):
                result.append(match.group(0))

    return result

'''
c) This functions reads all two part names from metadata file and returns them in a list
'''
def extract_two_part_names(path: Path):

    data = parse_metadata_file(path)
    pattern = re.compile(r'^[^-]+-[^-]+$')
    
    result = []

    for _, station_data in data.items():
        if(match := pattern.match(station_data['name'])):
            result.append(match.group(0))

    return result

'''
d) This function reads station names from metadata file and returns them in a list with following replacements:
' ' -> '_'
polish char -> latin char (ex. 'ą' -> 'a') 
'''
def transform_names(path: Path):

    data = parse_metadata_file(path)

    spaces_pattern = re.compile(r'\s+')
    polish_chars_pattern = re.compile(r'[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]')

    result = []

    for _, station_data in data.items():
        new_name = spaces_pattern.sub('_', station_data['name'])
        new_name = polish_chars_pattern.sub(lambda match: pl_latin_char_map[match.group(0)], new_name)
        result.append(new_name)

    return result

'''
e) This function checks whether all station which code ends with MOB has operation_type set to 'mobile'
It returns boolean information and all stations codes which don't meet this condition
'''

def verify_mobility_type(path: Path):

    data = parse_metadata_file(path)
    pattern = re.compile(r'.+MOB$')

    invalid_type_stations = []

    for station_code, station_data in data.items():
        if(match:=pattern.match(station_code)):
            if not (station_data['operation_type'] == 'mobilna'):
                invalid_type_stations.append((station_code, station_data['operation_type']))

    return not bool(invalid_type_stations), invalid_type_stations

'''
f) This function extracts three part '-' separated names and returns them as a list
'''
def extract_three_part_names(path: Path):

    data = parse_metadata_file(path)
    pattern = re.compile(r'^[^-]+-[^-]+-[^-]+$')
    
    result = []

    for _, station_data in data.items():
        if(match := pattern.match(station_data['name'])):
            result.append(match.group(0))

    return result


'''
g) This function extracts names consisting of ',' and ul. or al.
It returns them as a list.
'''
def extract_address_names(path: Path):

    data = parse_metadata_file(path)
    pattern = re.compile(r',.*?\b(?:ul\.|al\.)')
    
    result = []

    for _, station_data in data.items():
        if(pattern.search(name:=station_data['name'])):
            result.append(name)

    return result

if __name__ == "__main__":
    
    print('-'*50)

    print('a) EXTRACT DATES')
    extracted_dates = extract_dates(Path('lab5/data/stacje.csv'))
    print(extracted_dates[:5])
    print('-'*50)

    print('b) EXTRACT COORDS')
    extracted_coords = extract_coords(Path('lab5/data/stacje.csv'))
    print(extracted_coords[:5])
    print('-'*50)

    print('c) EXTRACT TWO-PART NAMES')
    extracted_two_part_names = extract_two_part_names(Path('lab5/data/stacje.csv'))
    print(extracted_two_part_names[:5])
    print('-'*50)

    print('d) TRANSFORM NAMES')
    transformed_names = transform_names(Path('lab5/data/stacje.csv'))
    print(transformed_names[:5])
    print('-'*50)

    print('e) VERIFY MOBILITY')
    is_valid, invalid_stations = verify_mobility_type(Path('lab5/data/stacje.csv'))
    print(f'Result: {is_valid}')
    print(invalid_stations[:5])
    print('-'*50)

    print('f) EXTRACT THREE-PART NAMES')
    extracted_three_part_names = extract_three_part_names(Path('lab5/data/stacje.csv'))
    print(extracted_three_part_names[:5])
    print('-'*50)

    print('g) EXTRACT ADDRESS NAMES')
    extracted_address_names = extract_address_names(Path('lab5/data/stacje.csv'))
    print(extracted_address_names[:5])
    print('-'*50)


