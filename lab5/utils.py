import csv

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

def parse_measurements_file(path):
    
    data = {}

    with open(path, mode = 'r', encoding='utf-8') as file:
        
        reader = csv.reader(file)
        
        next(reader) #stations numbers skip
        
        station_codes = next(reader)[1:]

        for station_code in station_codes:
            data[station_code] = {}

        for _ in range(4): #measurments data skip
            next(reader)

        for row in reader:
            
            if not row:
                continue

            date = row[0]
            values = row[1:]

            for station_code, str_value in zip (station_codes, values):
                #setting proper float value for non empty strings, None otherwise
                data[station_code][date] = float (str_value) if str_value.strip() else None

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

def parse_metadata_file(path):

    data = {}

    with open(path, mode = 'r', encoding='utf-8') as file:
        
        columns_names = ['id', 'code', 'international_code', 'name', 'old_code', 'launch_date', 'close_date', 'station_type', 'area_type', 'operation_type', 'voivodeship', 'locality', 'address', 'WGS84N', 'WGS84E']

        reader = csv.reader(file)
        
        next(reader) #header skip
        
        for row in reader:
        
            if not row or not (code := row[1].strip()):
                continue


            data[code] = {}

            #reading id
            data[code][columns_names[0]] = row[0].strip()

            #starting from third element to ommit station code which is second
            for str_value, column_name in zip (row[2:], columns_names[2:]):
                data[code][column_name] = str_value.strip()
            
    return data

pl_latin_char_map = {
        'ą':'a', 'ć':'c', 'ę':'e', 'ł':'l', 'ń':'n', 'ó':'o', 'ś':'s', 'ź':'z', 'ż':'z',
        'Ą':'A', 'Ć':'C', 'Ę':'E', 'Ł':'L', 'Ń':'N', 'Ó':'O', 'Ś':'S', 'Ź':'Z', 'Ż':'Z'
        }