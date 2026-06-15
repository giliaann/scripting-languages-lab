from pathlib import Path
import sys
from src.database import GTFSDatabase
from src.presenter import TransitPresenter
from src.service import TransitService
from src.views.gui import TransitGUI
from PySide6.QtWidgets import QApplication


def main() -> None:
    db_path = Path(__file__).parent / "data" / "database" / "moja_baza.sqlite"
    app = QApplication(sys.argv)
    db = GTFSDatabase(db_path)
    service = TransitService(db)
    view = TransitGUI()
    presenter = TransitPresenter(view, service)
    view.set_presenter(presenter)
    view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
