import csv
import logging

'''
Parsing measurements data files
Measurements file name: <year>_<measurand>_<frequency>.csv
Output format of function:
{   
    <station_code_0> : {date_0 : val0, date_1 : val1, date_2 : val2 ... }
    <station_code_1> : {date_0 : val0, date_1 : val1, date_2 : val2 ... }
    ...
}
'''

def parse_measurements_file(path, log = False):

    data = {}

    if not path.is_file():
        if log:
            logging.critical(f"File {path} does not exist or is not a file!")
        return data


    if log:
        logging.info(f"Opened file: {path}")

    with open(path, mode = 'r', encoding='utf-8') as file:
        
        reader = csv.reader(file)
        
        row = next(reader) #stations numbers skip
        
        if log:
            logging.debug(f"Read: {sum(len(s.encode('utf-8')) for s in row)} bytes")
        
        row = next(reader)

        if log:
            logging.debug(f"Read: {sum(len(s.encode('utf-8')) for s in row)} bytes")

        station_codes = row[1:]


        for station_code in station_codes:
            data[station_code] = {}

        for row in range(4):
            #measurments data skip
            row = next(reader)
            if row:
                logging.debug(f"Read: {sum(len(s.encode('utf-8')) for s in row)} bytes")

        for row in reader:
            if not row:
                continue

            if log:
                logging.debug(f"Read: {sum(len(s.encode('utf-8')) for s in row)} bytes")

            date = row[0]
            values = row[1:]

            for station_code, str_value in zip (station_codes, values):
                #setting proper float value for non empty strings, None otherwise
                data[station_code][date] = float (str_value) if str_value.strip() else None

    if log:
        logging.info(f"Closed file: {path}")

    return data

'''
Parsing stations metadata file
Stations metadata file name: stacje.csv
Output format of function:
{   
    <station_code_0> : {id : val, international_code : val, old_code : val, launch_date : YYYY-MM-DD, close_date : YYYY-MM-DD, 
    station_type : val, area_type: val, operation_type : val, voivodeship : val, locality : val, address : val, WGS84N : val, WGS84E : val}
    ...
}

'''

def parse_metadata_file(path, log = False):

    data = {}

    if not path.is_file():
        if log:
            logging.critical(f"File {path} does not exist or is not a file - cannot read metadata")
        return data

    if log:
        logging.info(f"Opened file: {path}")

    with open(path, mode = 'r', encoding='utf-8') as file:
        
        columns_names = ['id', 'code', 'international_code', 'name', 'old_code', 'launch_date', 'close_date', 'station_type', 'area_type', 'operation_type', 'voivodeship', 'locality', 'address', 'WGS84N', 'WGS84E']

        reader = csv.reader(file)
        
        row = next(reader) #header skip

        if log:
                logging.debug(f"Read: {sum(len(s.encode('utf-8')) for s in row)} bytes")
        
        for row in reader:
            
            if not row:
                continue
            
            if log:
                logging.debug(f"Read: {sum(len(s.encode('utf-8')) for s in row)} bytes")

            if not (code := row[1].strip()):
                continue


            data[code] = {}

            #reading id
            data[code][columns_names[0]] = row[0].strip()

            #starting from third element to ommit station code which is second
            for str_value, column_name in zip (row[2:], columns_names[2:]):
                data[code][column_name] = str_value.strip()

    if log:
        logging.info(f"Closed file: {path}")
            
    return data

pl_latin_char_map = {
        'ą':'a', 'ć':'c', 'ę':'e', 'ł':'l', 'ń':'n', 'ó':'o', 'ś':'s', 'ź':'z', 'ż':'z',
        'Ą':'A', 'Ć':'C', 'Ę':'E', 'Ł':'L', 'Ń':'N', 'Ó':'O', 'Ś':'S', 'Ź':'Z', 'Ż':'Z'
        }