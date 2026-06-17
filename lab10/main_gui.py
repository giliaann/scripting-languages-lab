from pathlib import Path
import sys
from src.database import GTFSDatabase
from src.presenter import TransitPresenter
from src.service import TransitService
from src.views.gui import TransitGUI
from PySide6.QtWidgets import QApplication
from src.databse_orm import GTFSDatabaseORM


def main(orm_mode: bool = False) -> None:

    if(orm_mode):
        db_path = Path(__file__).parent / "data" / "database" / "db_orm.sqlite"
        db = GTFSDatabaseORM(db_path)

    else:

        db_path = Path(__file__).parent / "data" / "database" / "moja_baza.sqlite"
        db = GTFSDatabase(db_path)

    app = QApplication(sys.argv)
    service = TransitService(db)
    view = TransitGUI()
    presenter = TransitPresenter(view, service)
    view.set_presenter(presenter)
    view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main(orm_mode=True)
