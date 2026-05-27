import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, 
                               QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, 
                               QLineEdit, QListWidget, QMessageBox)
from PySide6.QtCore import Qt

from LogManager import LogManager
from pathlib import Path


class TopBarWidget(QWidget):
    """Handles the file path input and open button."""
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)

        self.path_input = QLineEdit('/home/student/NASA')
        self.open_btn = QPushButton('Open')
        
        layout.addWidget(self.path_input)
        layout.addWidget(self.open_btn)


class LogListPanel(QWidget):
    """Handles the date filters and the list of logs (left side)."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # Filter Date Part
        filter_date_layout = QHBoxLayout()

        from_date_layout = QHBoxLayout()
        self.from_label = QLabel('From')
        self.from_date_text = QLineEdit('2019-01-22')
        from_date_layout.addWidget(self.from_label)
        from_date_layout.addWidget(self.from_date_text)
        filter_date_layout.addLayout(from_date_layout)

        to_date_layout = QHBoxLayout()
        self.to_label = QLabel('To')
        self.to_date_text = QLineEdit('2019-01-22')
        to_date_layout.addWidget(self.to_label)
        to_date_layout.addWidget(self.to_date_text)
        filter_date_layout.addLayout(to_date_layout)

        layout.addLayout(filter_date_layout)

        # Log List
        self.log_list = QListWidget()
        self.log_list.setTextElideMode(Qt.TextElideMode.ElideRight)
        self.log_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # USUNIĘTO stąd sztuczne generowanie 20 logów, żeby lista na start była czysta
        layout.addWidget(self.log_list)

        # page change buttons
        # page change buttons (wewnątrz __init__ klasy LogListPanel)
        page_btn_layout = QHBoxLayout()
        self.prev_page_btn = QPushButton('Previous page')
        self.next_page_btn = QPushButton('Next page')
        
        # Nowe elementy do skakania do konkretnej strony
        self.page_input = QLineEdit()
        self.page_input.setFixedWidth(40)  # Szerokość na max 3-4 cyfry
        self.page_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.total_pages_label = QLabel('/ 0')

        # Układamy elementy w paski w odpowiedniej kolejności:
        page_btn_layout.addWidget(self.prev_page_btn)
        page_btn_layout.addStretch()
        
        # Środkowy panel w stylu przeglądarki
        page_btn_layout.addWidget(self.page_input)
        page_btn_layout.addWidget(self.total_pages_label)
        
        page_btn_layout.addStretch()
        page_btn_layout.addWidget(self.next_page_btn)
        layout.addLayout(page_btn_layout)


class LogDetailPanel(QWidget):
    """Handles the grid view of specific log details (right side)."""
    def __init__(self):
        super().__init__()
        layout = QGridLayout(self)

        # Row 0: remote host
        layout.addWidget(QLabel('Remote host'), 0, 0)
        self.val_remote_host = QLineEdit('-')
        layout.addWidget(self.val_remote_host, 0, 1)

        # Row 1: date
        layout.addWidget(QLabel('Date'), 1, 0)
        self.val_date = QLineEdit('-')
        layout.addWidget(self.val_date, 1, 1, 1, 3) 

        # Row 2: time / timezone
        layout.addWidget(QLabel('Time'), 2, 0)
        self.val_time = QLineEdit('-')
        layout.addWidget(self.val_time, 2, 1)
        
        layout.addWidget(QLabel('Timezone:'), 2, 2)
        self.val_timezone = QLineEdit('-')
        layout.addWidget(self.val_timezone, 2, 3)

        # Row 3: status code / method
        layout.addWidget(QLabel('Status code:'), 3, 0)
        self.val_status = QLabel('-')
        layout.addWidget(self.val_status, 3, 1)

        layout.addWidget(QLabel('Method:'), 3, 2)
        self.val_method = QLabel('-')
        layout.addWidget(self.val_method, 3, 3)

        # Row 4: resource
        layout.addWidget(QLabel('Resource:'), 4, 0)
        self.val_resource = QLineEdit('-')
        layout.addWidget(self.val_resource, 4, 1, 1, 3)

        # Row 5: size
        layout.addWidget(QLabel('Size:'), 5, 0)
        self.val_size = QLabel('- Bytes')
        layout.addWidget(self.val_size, 5, 1, 1, 3)


class BottomBarWidget(QWidget):
    """Handles the pagination controls at the bottom."""
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)

        self.previous_btn = QPushButton('Previous')
        self.next_btn = QPushButton('Next')
        
        layout.addWidget(self.previous_btn)
        layout.addStretch()
        layout.addWidget(self.next_btn)


class MainWindow(QMainWindow):
    """Main application window that glues all components together."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Shrek log browser')
        self.resize(800, 450)

        container = QWidget()
        self.setCentralWidget(container)
        main_layout = QVBoxLayout(container)

        self.top_bar = TopBarWidget()
        self.log_list_panel = LogListPanel()
        self.log_detail_panel = LogDetailPanel()
        self.bottom_bar = BottomBarWidget()

        middle_layout = QHBoxLayout()
        middle_layout.addWidget(self.log_list_panel, stretch=1)
        middle_layout.addWidget(self.log_detail_panel, stretch=1)

        main_layout.addWidget(self.top_bar)
        main_layout.addLayout(middle_layout)
        main_layout.addWidget(self.bottom_bar)

        # funkcjonalnosci
        self.log_manager = LogManager(page_size=1000)

        self.top_bar.open_btn.clicked.connect(self.load_file_clicked)
        self.log_list_panel.log_list.currentRowChanged.connect(self.log_selection_changed)
        self.bottom_bar.next_btn.clicked.connect(self.next_log)
        self.bottom_bar.previous_btn.clicked.connect(self.previous_log)
        self.log_list_panel.next_page_btn.clicked.connect(self.next_page)
        self.log_list_panel.prev_page_btn.clicked.connect(self.previous_page)

        # Wygaszenie wszystkich przycisków nawigacyjnych na starcie
        self.update_log_nav_btn()
        self.update_page_nav_btn()

        # (wewnątrz __init__ klasy MainWindow obok innych connectów)
        self.log_list_panel.page_input.returnPressed.connect(self.jump_to_page)
        
        # Na start pole wpisywania też jest wyłączone
        self.log_list_panel.page_input.setEnabled(False)


    def load_file_clicked(self):
        path_str = self.top_bar.path_input.text().strip()
        if not path_str:
            QMessageBox.warning(self, 'No given sciezka', 'Enter path to the HTTP log file before clicking open')
            return
        
        path = Path(path_str)

        try:
            raw_lines = self.log_manager.load_file(path)
            if not raw_lines:
                QMessageBox.information(self, 'Empty file', 'Choosen file has no logs')
                self.log_list_panel.log_list.clear()
                self.update_log_nav_btn()
                self.update_page_nav_btn()
                return
            
            self.log_list_panel.log_list.clear()
            self.log_list_panel.log_list.addItems(raw_lines)
            
            # POPRAWKA: sprawdzenie długości listy za pomocą len()
            if len(raw_lines) > 0:
                self.log_list_panel.log_list.setCurrentRow(0)
            
            self.update_page_nav_btn()

        except FileNotFoundError:
            QMessageBox.critical(self, 'Error: File not found', f'File of path: {path} does not exist')
        except PermissionError:
            QMessageBox.critical(self, 'Error: NO permission to open file', f'You do not have permission to open file {path}')
        except IsADirectoryError:
            QMessageBox.critical(self, 'Error: Path is a directory', f'Given path: {path} is a directory, not a file')
        except Exception as e:
            QMessageBox.critical(self, 'Critical error', f'Unexpected error while loading file from: {path}\n{str(e)}')


    def log_selection_changed(self, index: int):
        # KROK 1: Zabezpieczenie przed indeksem -1 (czyszczenie listy)
        if index < 0:
            self.update_log_nav_btn()
            return

        # KROK 2: Aktualizacja stanu dolnych przycisków na podstawie nowej pozycji
        self.update_log_nav_btn()
        
        # KROK 3: Pobranie sparsowanego logu z managera i wyświetlenie go w GUI
        parsed_log = self.log_manager.get_parsed_log_at(index)

        if parsed_log:
            self.log_detail_panel.val_remote_host.setText(getattr(parsed_log, 'remote_host', 'N/A'))
            self.log_detail_panel.val_date.setText(getattr(parsed_log, 'date_only', 'N/A'))
            self.log_detail_panel.val_time.setText(getattr(parsed_log, 'time_only', 'N/A'))
            self.log_detail_panel.val_timezone.setText(getattr(parsed_log, 'timezone', 'N/A'))
            self.log_detail_panel.val_status.setText(str(getattr(parsed_log, 'status', 'N/A')))
            self.log_detail_panel.val_method.setText(getattr(parsed_log, 'method', 'N/A'))
            self.log_detail_panel.val_resource.setText(getattr(parsed_log, 'resource', 'N/A'))
            self.log_detail_panel.val_size.setText(f"{getattr(parsed_log, 'size', '0')} Bytes")


    def load_page(self, page_num: int):
        """Pomocnicza metoda ładująca określoną stronę do listy i odświeżająca GUI."""
        raw_lines = self.log_manager.load_page(page_num)
        
        self.log_list_panel.log_list.clear()
        self.log_list_panel.log_list.addItems(raw_lines)
        
        if len(raw_lines) > 0:
            self.log_list_panel.log_list.setCurrentRow(0)
            
        self.update_page_nav_btn()


    def next_log(self):
        current_row = self.log_list_panel.log_list.currentRow()
        if current_row < self.log_list_panel.log_list.count() - 1:
            self.log_list_panel.log_list.setCurrentRow(current_row + 1)


    def previous_log(self):
        current_row = self.log_list_panel.log_list.currentRow()
        if current_row > 0:
            self.log_list_panel.log_list.setCurrentRow(current_row - 1)


    def next_page(self):
        """Pobiera z managera kolejną stronę danych (o ile istnieje)."""
        curr = self.log_manager.current_page
        # Zakładam, że pole w LogManagerze nazywa się total_pages lub pages_count (dostosuj jeśli trzeba)
        total = self.log_manager.pages_count 
        
        if curr < total - 1:
            self.load_page(curr + 1)


    def previous_page(self):
        """Pobiera z managera poprzednią stronę danych (o ile istnieje)."""
        curr = self.log_manager.current_page
        if curr > 0:
            self.load_page(curr - 1)


    def update_log_nav_btn(self):
        """Zarządza dolnymi przyciskami (skakanie po linijkach)."""
        curr = self.log_list_panel.log_list.currentRow()
        total = self.log_list_panel.log_list.count()
        self.bottom_bar.previous_btn.setEnabled(curr > 0)
        self.bottom_bar.next_btn.setEnabled(curr < total - 1 and total > 0)


    def update_page_nav_btn(self):
        """Zarządza przyciskami pod listą (skakanie po stronach)."""
        curr = self.log_manager.current_page
        total = self.log_manager.pages_count
        self.log_list_panel.prev_page_btn.setEnabled(curr > 0)
        self.log_list_panel.next_page_btn.setEnabled(curr < total - 1 and total > 0)
        
        # Dodatkowo aktualizujemy tytuł okna informacją o stronie
        if total > 0:
            self.setWindowTitle(f'Shrek log browser - Page {curr + 1} of {total}')
        else:
            self.setWindowTitle('Shrek log browser - No file loaded')

    def jump_to_page(self):
        """Wywoływane, gdy użytkownik wpisze numer strony i wciśnie Enter."""
        text = self.log_list_panel.page_input.text().strip()
        total = self.log_manager.pages_count

        if not text or total == 0:
            return

        try:
            # Użytkownik myśli w kategoriach stron od 1, indeksujemy od 0
            target_page = int(text) - 1
            
            if 0 <= target_page < total:
                self.load_page(target_page)
            else:
                QMessageBox.warning(
                    self, 
                    "Niepoprawny numer", 
                    f"Wpisz numer strony w przedziale od 1 do {total}."
                )
                # Resetujemy tekst pola do aktualnej poprawnej strony
                self.log_list_panel.page_input.setText(str(self.log_manager.current_page + 1))
                
        except ValueError:
            QMessageBox.warning(self, "Błąd", "Wprowadzona wartość musi być liczbą całkowitą.")
            self.log_list_panel.page_input.setText(str(self.log_manager.current_page + 1))


    def update_page_nav_btn(self):
        """Zarządza przyciskami pod listą oraz polem skoku do strony."""
        curr = self.log_manager.current_page
        total = self.log_manager.pages_count
        
        # Włączamy lub wyłączamy pole tekstowe w zależności od tego, czy plik jest załadowany
        has_pages = total > 0
        self.log_list_panel.page_input.setEnabled(has_pages)

        self.log_list_panel.prev_page_btn.setEnabled(curr > 0)
        self.log_list_panel.next_page_btn.setEnabled(curr < total - 1 and has_pages)
        
        # Aktualizacja wartości w stylu przeglądarki (np. "5" / "24")
        if has_pages:
            self.log_list_panel.page_input.setText(str(curr + 1))
            self.log_list_panel.total_pages_label.setText(f"/ {total}")
            self.setWindowTitle(f'Shrek log browser - Page {curr + 1} of {total}')
        else:
            self.log_list_panel.page_input.clear()
            self.log_list_panel.total_pages_label.setText("/ 0")
            self.setWindowTitle('Shrek log browser - No file loaded')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())