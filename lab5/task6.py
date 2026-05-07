import typer
from typing import Annotated, Literal
from datetime import datetime
from pathlib import Path
from group_measurement_files_by_key import group_measurement_files_by_key
from utils import parse_measurements_file, parse_metadata_file
import random


MEASUREMENTS_DIR = Path('lab5/data/measurements')
METADATA_FILE_PATH = Path('lab5/data/stacje.csv')

app = typer.Typer(help="System analizy danych pomiarowych (ale ten w Typer)")


class ContextState:
    def __init__(self):
        self.measurand: measurement_types | None = None
        self.freq: frequency_types | None = None
        self.start: datetime | None = None
        self.end: datetime | None = None

state = ContextState()


measurement_types = Literal[
    'NO2',
    'IP(PM10)',
    'Depozycja',
    'NOx',
    'C6H6',
    'Hg(TGM)',
    'SO2',
    'formaldehyd',
    'BaA(PM10)',
    'Jony',
    'Pb(PM10)',
    'BbF(PM10)',
    'NO',
    'DBahA(PM10)',
    'BjF(PM10)',
    'PM25',
    'SO2',
    'NO2',
    'BkF(PM10)',
    'PM10',
    'Ni(PM10)',
    'Cd(PM10)',
    'O3',
    'BaP(PM10)',
    'CO',
    'PM10',
    'As(PM10)',
    'PM25',
    'PrekursoryZielonka'
]

frequency_types = Literal[
    '1g',
    '24g'
]


@app.callback()
def main(
        measurand: Annotated[measurement_types, typer.Option(..., help="Measurand (ex. CO)")],
        freq: Annotated[frequency_types, typer.Option(..., help="Frequency (ex. 1g or 24g)")],
        start: Annotated[datetime, typer.Option(..., formats=["%Y-%m-%d"], help="Start date (ex. 2023-01-01)")],
        end: Annotated[datetime, typer.Option(..., formats=["%Y-%m-%d"], help="End date (ex. 2023-12-31)")],
):
    if start >= end:
        raise typer.BadParameter("Start date must be before end date")
    
    state.measurand = measurand
    state.freq = freq
    state.start = start
    state.end = end


@app.command()
def random_station():
    """
    Prints name and address of random station measuring given measurand with given frequency in given period
    """

    measurements_dict = group_measurement_files_by_key(MEASUREMENTS_DIR)
    found_paths = (found_path for (y,m,f), found_path in measurements_dict.items() if str(state.start.year) <= y <= str(state.end.year) and state.freq == f and state.measurand == m)

    if not found_paths:
        typer.secho(f'No station measures {state.measurand} in period ({state.start} - {state.end}) at frequency {state.freq}', fg=typer.colors.YELLOW)
        raise typer.Exit(0)
    
    station_codes = set()
    
    for found_path in found_paths:
        measurements = parse_measurements_file(found_path, True)

        for station_code, data in measurements.items():
            for date, value in data.items():
                if value:
                    try:
                        date = datetime.strptime(date, "%m/%d/%y %H:%M")
                    except ValueError:
                        typer.secho(f"Cannot parse date {date}", fg=typer.colors.YELLOW)
                        continue # TODO logowanie?
                    if state.start <= date <= state.end:
                        station_codes.add(station_code)
                        break
    if not station_codes:
        typer.secho(f"No station measures {state.measurand} between {state.start} and {state.end}", fg=typer.colors.YELLOW)
        raise typer.Exit(0)
    
    metadata = parse_metadata_file(METADATA_FILE_PATH, True)
    random_station_code = random.choice(tuple(station_codes))
    station_data = metadata[random_station_code]
    typer.echo(f"{station_data['name']} {station_data['voivodeship']} {station_data['locality']} {station_data['address']}")



@app.command()
def stats_for_station(
    station: Annotated[str, typer.Argument(..., help="Station code")], # callback?
):
    """
    Prints mean and standard deviation of measurements for given station, measurand, frequency and period
    """
    typer.echo(f"Statystyki dla stacji: {station}")



if __name__ == "__main__":
    app()