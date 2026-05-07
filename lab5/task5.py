import argparse
import logging
import sys
import random
from utils import parse_measurements_file, parse_metadata_file
from datetime import datetime
from pathlib import Path
from group_measurement_files_by_key import group_measurement_files_by_key
import numpy as np

MEASUREMENTS_DIR = 'lab5/data/measurements'
METADATA_FILE_PATH = 'lab5/data/stacje.csv'

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    #Stodut handler (DEBUG, INFO, WARNING)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    #Filter - leave only level lower than ERROR
    stdout_handler.addFilter(lambda record: record.levelno < logging.ERROR)
    stdout_handler.setFormatter(formatter)

    #Stderr handler (ERROR, CRITICAL)
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR)
    #Filter - leave only level higher or equal than ERROR
    stderr_handler.addFilter(lambda record: record.levelno >= logging.ERROR)
    stderr_handler.setFormatter(formatter)

    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)

def validate_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        raise argparse.ArgumentTypeError(f"Ivalid date format: {date_str}. Use YYYY-MM-DD.")

def validate_measurand(value):
    return value #idk how

'''
This function returns list of pairs (<station_code>, <station_meaurement_data_dict>) of stations that measures
given measurand with given frequency in given period
'''

def find_valid_stations(args):
    measurements_dict = group_measurement_files_by_key(Path(MEASUREMENTS_DIR), True)
    
    measurand = args.measurand
    year_start = str(args.start.year)
    year_end = str(args.end.year)
    freq = args.freq

    found_paths = [found_path for (y,m,f), found_path in measurements_dict.items() if ((year_end == y or year_start == y) and freq == f and measurand == m)]

    valid_stations = []

    if not found_paths:
        logging.warning(f'No station measures {measurand} in years {year_start, year_end} with freq {freq}')
        return valid_stations

    for found_path in found_paths:
        measurements = parse_measurements_file(Path(found_path), True)
        
        for station_code, data in measurements.items():
            
            for date, value in data.items():

                if value:
                    try:
                        date =  datetime.strptime(date, '%m/%d/%y %H:%M').date()
                    except ValueError:
                        logging.warning(f'Cannot parse date: {date}')
                        continue
                    if args.start < date < args.end:
                        valid_stations.append((station_code, data))
                        break

    if not valid_stations:
        logging.warning(f'No station measures {args.measurand} between {args.start} and {args.end}')
    
    return valid_stations


def random_measuring_station_data(args):
    
    valid_stations = find_valid_stations(args)

    if not valid_stations:
        return None, None

    metadata = parse_metadata_file(Path(METADATA_FILE_PATH), True)

    if not metadata:
        return None, None

    random_station_code = random.choice(valid_stations)

    station_data = metadata[random_station_code[0]]

    return station_data['name'], f'{station_data['voivodeship'], station_data['locality'], station_data['address']}'


def stats_for_station(args):
    
    valid_stations = find_valid_stations(args)

    if not valid_stations:
        return None,None
    
    found_station = None

    for station_code, data in valid_stations:
        if station_code == args.station_code.strip():
            found_station = (station_code, data)
            break

    if not found_station:
        logging.warning(f'Station {args.station_code} does not measure {args.measurand} between {args.start} and {args.end} with freq {args.freq}')
        return None, None
    

    measured_values = []

    for date, value in found_station[1].items():
        if value:
            try:
                date =  datetime.strptime(date, '%m/%d/%y %H:%M').date()
            except ValueError:
                logging.warning(f'Cannot parse date: {date}')
                continue
            if args.start < date < args.end:
                measured_values.append(value)

    if not measured_values:
        logging.warning(f'Station {args.station_code} does not measure {args.measurand} between {args.start} and {args.end} with freq {args.freq}')
        return None, None

    return np.mean(measured_values), np.std(measured_values, ddof=1)


def main():
    setup_logging()
    
    parser = argparse.ArgumentParser(description="System analizy danych pomiarowych.")
    
    parser.add_argument("--measurand", type=validate_measurand, required=True, help="Measurand (ex. CO)")
    parser.add_argument("--freq", choices=['1g', '24g'], required=True, help="Frequency (1g or 24g)")
    parser.add_argument("--start", type=validate_date, required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=validate_date, required=True, help="End date (YYYY-MM-DD)")

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("random", help="Print name and address of random station measuring given measurand with given frequency in given period")

    stats_parser = subparsers.add_parser("stats", help="Stats of selected station measuring given measurand with given frequency in given period")
    stats_parser.add_argument("station_code", help="station code")

    args = parser.parse_args()

    parse_metadata_file(Path('lab5\data\stacje.csv'), True)

    if args.command == "random":
        name, address = random_measuring_station_data(args)
        if name or address:
            print(f'Random name and addres of station: \n {name}, {address}')
    elif args.command == "stats":
        mean, std = stats_for_station(args)
        if mean and std:
            print(f'Statistics for {args.station_code} measurement of {args.measurand} between {args.start} and {args.end}:\nmean = {mean}\nstd = {std}')

if __name__ == "__main__":
    main()
