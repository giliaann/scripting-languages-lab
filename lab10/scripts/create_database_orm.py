import sys
from pathlib import Path
from sqlalchemy import create_engine
from src.models import Base

def create_database(db_path: Path) -> None:
    engine = create_engine(f"sqlite:///{db_path.as_posix()}", echo=False)
    
    Base.metadata.create_all(engine)
    
    print(f"Data base saved: {db_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: uv run {Path(sys.argv[0]).name} <database name>", file=sys.stderr)
        sys.exit(1)

    try:
        db_path = Path(__file__).parent.parent / 'data' / 'database'/ Path(sys.argv[1]).with_suffix(".sqlite")
        create_database(db_path)
    except Exception as e:
        print(f"Error occured: \n{e}", file=sys.stderr)
        sys.exit(1)