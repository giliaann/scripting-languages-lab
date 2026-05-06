import argparse
import logging
import sys
import random
from utils import parse_measurements_file, parse_metadata_file
from datetime import datetime
from pathlib import Path
from group_measurement_files_by_key import group_measurement_files_by_key

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

def random_measuring_station_data(args):
    
    measurements_dict = group_measurement_files_by_key(Path(MEASUREMENTS_DIR))
    
    measurand = args.measurand
    year = str(args.start.year)
    freq = args.freq

    found_paths = [found_path for (y,m,f), found_path in measurements_dict.items() if (year == y and freq == f and measurand == m)]

    if not found_paths:
        logging.warning(f'No station measures {measurand} in year {year}')
        return '',''
    
    valid_stations_codes = []

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
                        valid_stations_codes.append(station_code)
                        break

    if not valid_stations_codes:
        logging.warning(f'No station measures {measurand} between {args.start} and {args.end}')
        return '',''

    metadata = parse_metadata_file(Path(METADATA_FILE_PATH), True)

    random_station_code = random.choice(valid_stations_codes)

    station_data = metadata[random_station_code]

    return station_data['name'], f'{station_data['voivodeship'], station_data['locality'], station_data['address']}'


def stats_for_station(args):
    pass
    

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
        print(f'Random name and addres of station: \n {random_measuring_station_data(args)}')
    elif args.command == "stats":
        stats_for_station()

if __name__ == "__main__":
    main()
