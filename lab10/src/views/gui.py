from src.presenter import TransitPresenter
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QLineEdit,
    QFrame,
    QMessageBox,
    QSplitter,
    QGridLayout,
    QScrollArea,
)
from PySide6.QtCore import Qt, QTimer, Slot


class StopListWidgetItem(QWidget):
    """Niestandardowy wiersz listy: Nazwa + ID pod spodem w innym kolorze"""
    def __init__(self, stop_id: str, stop_name: str, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(4)
        
        self.name_label = QLabel(stop_name)
        self.name_label.setStyleSheet("font-weight: bold; font-size: 13px; color: #ffffff;")
        
        self.id_label = QLabel(f"ID: {stop_id}")
        self.id_label.setStyleSheet("color: #8a8a93; font-size: 11px;")

        layout.addWidget(self.name_label)
        layout.addWidget(self.id_label)


class StatCard(QFrame):
    """Estetyczny kafelek dla pojedynczych metryk"""
    def __init__(self, title: str, value: str = "-"):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: #2c2c2e;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setSpacing(2)
        
        self.title_label = QLabel(title.upper())
        self.title_label.setStyleSheet("color: #8a8a93; font-size: 10px; font-weight: bold;")
        
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet("color: #007aff; font-size: 18px; font-weight: bold;")
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)

    def set_value(self, value: str):
        self.value_label.setText(str(value))


class TransitGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.presenter: TransitPresenter | None = None
        self.setWindowTitle("Transit Stop Explorer")
        self.resize(1400, 800)

        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.setInterval(300)
        self.search_timer.timeout.connect(self._trigger_search)

        self.setStyleSheet("""
            QMainWindow { background-color: #1c1c1e; }
            QLabel { color: #ffffff; }
        """)

        self._build_ui()

    def _on_search_text_changed(self) -> None:
        self.search_timer.start()

    def _trigger_search(self) -> None:
        if self.presenter:
            self.presenter.on_search(self.search_input.text())

    def set_presenter(self, presenter: TransitPresenter) -> None:
        self.presenter = presenter
        self.search_input.textChanged.connect(self._on_search_text_changed)
        self.stop_list.currentItemChanged.connect(self._on_stop_selection_changed)
        self.presenter.on_search("")

    def _on_stop_selection_changed(self, current: QListWidgetItem, previous: QListWidgetItem) -> None:
        if not self.presenter:
            return
        if not current:
            self.presenter.on_stop_selected(None, "")
            return
            
        stop_id = current.data(Qt.UserRole)
        widget = self.stop_list.itemWidget(current)
        stop_name = widget.name_label.text() if widget else ""
        
        self.presenter.on_stop_selected(stop_id, stop_name)

    def _build_ui(self) -> None:
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self._create_left_panel())
        splitter.addWidget(self._create_right_panel())
        splitter.setSizes([350, 1050])
        splitter.setContentsMargins(10, 10, 10, 10)
        self.setCentralWidget(splitter)

    def _create_left_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search for stops...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #2c2c2e;
                border: 1px solid #3a3a3c;
                border-radius: 8px;
                padding: 8px 12px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus { border: 1px solid #007aff; }
        """)
        
        self.stop_list = QListWidget()
        self.stop_list.setStyleSheet("""
            QListWidget { background-color: #2c2c2e; border: 1px solid #3a3a3c; border-radius: 8px; }
            QListWidget::item { border-bottom: 1px solid #3a3a3c; }
            QListWidget::item:selected { background-color: #3a3a3c; border-radius: 6px; }
        """)

        layout.addWidget(self.search_input)
        layout.addWidget(self.stop_list)
        return panel
    
    def _create_right_panel(self) -> QWidget:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        panel = QWidget()
        panel.setStyleSheet("background-color: #1c1c1e;")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(15, 0, 15, 0)
        layout.setSpacing(15)

        self.stop_name = QLabel("Select a stop to see details")
        self.stop_name.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff;")
        self.stop_name.setWordWrap(True)
        
        self.stop_id_label = QLabel("")
        self.stop_id_label.setStyleSheet("font-size: 14px; color: #8a8a93;")
        
        layout.addWidget(self.stop_name)
        layout.addWidget(self.stop_id_label)

        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setSpacing(10)

        self.card_lines = StatCard("Number of lines")
        self.card_departures = StatCard("Departures")
        self.card_earliest = StatCard("Earliest Departure")
        self.card_latest = StatCard("Latest Departure")

        grid_layout.addWidget(self.card_lines, 0, 0)
        grid_layout.addWidget(self.card_departures, 0, 1)
        grid_layout.addWidget(self.card_earliest, 1, 0)
        grid_layout.addWidget(self.card_latest, 1, 1)
        layout.addWidget(grid_widget)

        dir_title = QLabel("Top Directions")
        dir_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff; margin-top: 10px;")
        layout.addWidget(dir_title)

        self.top_directions_list = QListWidget()
        self.top_directions_list.setStyleSheet(self._list_style())
        # FIX 1: Blokujemy rozciąganie listy kierunków (wystarczy na ok. 3-4 pozycje)
        self.top_directions_list.setMaximumHeight(150) 
        layout.addWidget(self.top_directions_list)

        next_title = QLabel("Next Departures")
        next_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff; margin-top: 10px;")
        layout.addWidget(next_title)

        self.next_departures_list = QListWidget()
        self.next_departures_list.setStyleSheet(self._list_style())
        # Opcjonalnie: możesz też ustawić minimalną wysokość dla najbliższych odjazdów, by były większe
        self.next_departures_list.setMinimumHeight(200) 
        layout.addWidget(self.next_departures_list)
        
        # FIX 2: Zastępujemy addSpacing() elastycznym separatorem stretch
        layout.addStretch()

        scroll.setWidget(panel)
        return scroll

    def _list_style(self) -> str:
        return """
            QListWidget {
                background-color: #2c2c2e;
                border: 1px solid #3a3a3c;
                border-radius: 8px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                color: #ffffff;
                border-bottom: 1px solid #3a3a3c;
            }
            QListWidget::item:last { border-bottom: none; }
        """

    @Slot(list)
    def show_stop_list(self, stops: list[tuple[str, str]]) -> None:
        self.stop_list.blockSignals(True)
        self.stop_list.clear()
        
        for stop_id, stop_name in stops:
            item = QListWidgetItem(self.stop_list)
            custom_widget = StopListWidgetItem(stop_id, stop_name)
            item.setSizeHint(custom_widget.sizeHint())
            item.setData(Qt.UserRole, stop_id)
            
            self.stop_list.addItem(item)
            self.stop_list.setItemWidget(item, custom_widget)
            
        self.stop_list.blockSignals(False)

    @Slot(object)
    def show_stats(self, stats) -> None:
        # Nagłówek główny
        self.stop_name.setText(stats.stop_name)
        self.stop_id_label.setText(f"ID: {stats.stop_id}")
        
        # Przypisanie wartości do kafelków metryk
        self.card_lines.set_value(str(stats.line_count))
        self.card_departures.set_value(str(stats.departure_count))
        self.card_earliest.set_value(stats.earliest_departure)
        self.card_latest.set_value(stats.latest_departure)

        # Aktualizacja listy najczęstszych kierunków
        self.top_directions_list.clear()
        for headsign, count in stats.top_directions:
            self.top_directions_list.addItem(f"🎯 {headsign}  ({count} trips)")

        # Aktualizacja listy najbliższych odjazdów
        self.next_departures_list.clear()
        for line, headsign, time in stats.next_n_departures:
            self.next_departures_list.addItem(f"🚌 Line {line:<6} ➔  {headsign:<25} at {time}")

    @Slot()
    def clear_stats(self) -> None:
        self.stop_name.setText("Select a stop to see details")
        self.stop_id_label.setText("")
        self.card_lines.set_value("-")
        self.card_departures.set_value("-")
        self.card_earliest.set_value("-")
        self.card_latest.set_value("-")
        self.top_directions_list.clear()
        self.next_departures_list.clear()

    @Slot(str)
    def show_error(self, message: str) -> None:
        QMessageBox.warning(self, "Error", message)