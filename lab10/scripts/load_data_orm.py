import sys
import zipfile
import csv
import io
from pathlib import Path
from itertools import batched
from typing import Type

from sqlalchemy import create_engine, insert
from sqlalchemy.orm import Session
from src.models import Base, Stop, Route, Calendar, Trip, StopTime

def load_table_from_zip(
    zip_file: zipfile.ZipFile,
    file_name: str,
    session: Session,
    model_class: Type[Base],
    batch_size: int = 50_000
) -> None:
    #
    if file_name not in zip_file.namelist():
        return

    print(f"Loading {model_class.__tablename__}...")
    
    valid_columns = model_class.__table__.columns.keys()
        
    with zip_file.open(file_name) as f:
        text_file = io.TextIOWrapper(f, encoding='utf-8-sig')
        reader = csv.DictReader(text_file)
            
        for batch in batched(reader, n=batch_size):
           
            filtered_batch = [
                {key: value for key, value in row.items() if key in valid_columns}
                for row in batch
            ]
                
        
            session.execute(insert(model_class), filtered_batch)
            session.commit()

def load_data(zip_path: Path, db_path: Path) -> None:
    engine = create_engine(
        f"sqlite:///{db_path.as_posix()}", 
    )
    
    # Enable FK constraints
    with engine.connect() as connection:
        connection.exec_driver_sql("PRAGMA foreign_keys = ON")

    with Session(engine) as session, zipfile.ZipFile(zip_path, 'r') as archive:
        # Load base tables
        load_table_from_zip(archive, 'stops.txt', session, Stop)
        load_table_from_zip(archive, 'routes.txt', session, Route)
        load_table_from_zip(archive, 'calendar.txt', session, Calendar)
        
        # Load dependent tables
        load_table_from_zip(archive, 'trips.txt', session, Trip)
        load_table_from_zip(archive, 'stop_times.txt', session, StopTime, batch_size=100_000)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(1)

    data_path = Path(__file__).parent.parent / 'data'

    archive_path = data_path / Path(sys.argv[1])
    db_path = data_path / 'database'/ Path(sys.argv[2]).with_suffix(".sqlite")
    
    load_data(archive_path, db_path)