import sys
from pathlib import Path
from dataclasses import dataclass
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, 
                               QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, 
                               QLineEdit, QListWidget, QMessageBox)
from PySide6.QtCore import Qt

# ==============================================================================
# 0. MODEL LAYER & UTILS PLACEHOLDERS
# ==============================================================================

@dataclass
class HTTPLog:
    """Placeholder for your actual HTTPLog structure from utils.py"""
    remote_host: str
    date: str
    time: str
    timezone: str
    status: str
    method: str
    resource: str
    size: str


def parse_http_log(raw_line: str) -> HTTPLog:
    """
    Placeholder for your actual parse_http_log logic.
    Replace this import/function with your real implementation.
    """
    # Simple regex mock to split the string just so the UI displays data
    try:
        host = raw_line.split(" ")[0]
        return HTTPLog(
            remote_host=host,
            date="2019-01-22",
            time="03:56:51",
            timezone="Asia/Tehran",
            status="200",
            method="GET",
            resource="/image/50995/productModel/200x200",
            size="2244"
        )
    except Exception:
        return HTTPLog("Error", "Error", "Error", "Error", "Error", "Error", "Error", "0")


class LogManager:
    def __init__(self, page_size: int = 1000):
        self._raw_lines: list[str] = []
        self.current_file_path: Path | None = None
        
        # Pagination Settings
        self.page_size = page_size
        self.current_page = 0

    def load_file(self, file_path: Path) -> list[str]:
        self.current_file_path = file_path
        self.current_page = 0
        self._raw_lines = []

        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            self._raw_lines = [line.strip() for line in f if line.strip()]

        return self.get_current_page_lines()

    def get_current_page_lines(self) -> list[str]:
        """Returns only the chunk of lines for the active page."""
        start = self.current_page * self.page_size
        end = start + self.page_size
        return self._raw_lines[start:end]

    def get_parsed_log_at(self, index_on_page: int) -> HTTPLog | None:
        """Translates current page index to global array index and returns parsed log."""
        global_index = (self.current_page * self.page_size) + index_on_page
        if 0 <= global_index < len(self._raw_lines):
            raw_line = self._raw_lines[global_index]
            return parse_http_log(raw_line)
        return None

    def total_pages(self) -> int:
        if not self._raw_lines:
            return 0
        return (len(self._raw_lines) + self.page_size - 1) // self.page_size

    def total_count(self) -> int:
        return len(self._raw_lines)


# ==============================================================================
# 1. GUI COMPONENTS LAYER
# ==============================================================================

class TopBarWidget(QWidget):
    """Handles the file path input and open button."""
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.path_input = QLineEdit('/home/student/NASA')
        self.open_btn = QPushButton('Open')
        
        layout.addWidget(self.path_input)
        layout.addWidget(self.open_btn)


class LogListPanel(QWidget):
    """Handles the date filters and the list of logs (left side)."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

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
        layout.addWidget(self.log_list)


class LogDetailPanel(QWidget):
    """Handles the grid view of specific log details (right side)."""
    def __init__(self):
        super().__init__()
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Row 0: remote host
        layout.addWidget(QLabel('Remote host'), 0, 0)
        self.val_remote_host = QLineEdit()
        layout.addWidget(self.val_remote_host, 0, 1)

        # Row 1: date
        layout.addWidget(QLabel('Date'), 1, 0)
        self.val_date = QLineEdit()
        layout.addWidget(self.val_date, 1, 1, 1, 3) 

        # Row 2: time / timezone
        layout.addWidget(QLabel('Time'), 2, 0)
        self.val_time = QLineEdit()
        layout.addWidget(self.val_time, 2, 1)
        
        layout.addWidget(QLabel('Timezone:'), 2, 2)
        self.val_timezone = QLineEdit()
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
        self.val_resource = QLineEdit()
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
        layout.setContentsMargins(0, 0, 0, 0)

        self.previous_btn = QPushButton('Previous Page')
        self.next_btn = QPushButton('Next Page')
        
        layout.addWidget(self.previous_btn)
        layout.addStretch()
        layout.addWidget(self.next_btn)


# ==============================================================================
# 2. ORCHESTRATION LAYER (MAIN WINDOW)
# ==============================================================================

class MainWindow(QMainWindow):
    """Main application window that glues all components together."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Shrek log browser')
        self.resize(800, 450)

        # 1. Initialize the Optimized Model Manager (1000 lines per page chunk)
        self.log_manager = LogManager(page_size=1000)

        # 2. Setup the UI layout
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

        # 3. Connect Signals to Slots (Functional glue logic)
        self.top_bar.open_btn.clicked.connect(self.load_file_clicked)
        self.log_list_panel.log_list.currentRowChanged.connect(self.log_selection_changed)
        self.bottom_bar.next_btn.clicked.connect(self.next_page)
        self.bottom_bar.previous_btn.clicked.connect(self.previous_page)

        # Initially gray out buttons because no file is loaded yet
        self.update_navigation_buttons()

    # --- LOGIC SLOTS ---

    def load_file_clicked(self):
        """Validates file path, handles errors, and feeds chunks into the UI."""
        sciezka_str = self.top_bar.path_input.text().strip()
        
        if not sciezka_str:
            QMessageBox.warning(self, "Missing Path", "Please enter a file path first.")
            return

        sciezka = Path(sciezka_str)

        try:
            # Load file and grab only the first page chunk
            current_chunk = self.log_manager.load_file(sciezka)
            
            if not current_chunk:
                QMessageBox.information(self, "Empty File", "The file is valid but contains no records.")
                self.log_list_panel.log_list.clear()
                self.update_navigation_buttons()
                return

            # Display the page elements
            self.display_current_page(current_chunk)
            self.update_navigation_buttons()

        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"The file under path:\n\"{sciezka}\"\ndoes not exist.")
        except OSError:
            QMessageBox.critical(self, "Path Format Error", "The path string contains characters illegal in your file system.")
        except PermissionError:
            QMessageBox.critical(self, "Permission Denied", f"Insufficient system privileges to open:\n\"{sciezka}\"")
        except Exception as e:
            QMessageBox.critical(self, "Critical Error", f"An unexpected error occurred:\n{str(e)}")

    def display_current_page(self, lines: list[str]):
        """Helper function to load lines smoothly without GUI blocking."""
        self.log_list_panel.log_list.clear()
        self.log_list_panel.log_list.addItems(lines)
        
        # Instantly select the first row on the fresh page chunk
        if lines:
            self.log_list_panel.log_list.setCurrentRow(0)

    def log_selection_changed(self, index: int):
        """Fires whenever user selects another row inside the list view."""
        if index < 0:
            return

        # Fetch the parsed element data securely via translated index mapping
        parsed_log = self.log_manager.get_parsed_log_at(index)
        
        if parsed_log:
            self.log_detail_panel.val_remote_host.setText(getattr(parsed_log, 'remote_host', 'N/A'))
            self.log_detail_panel.val_date.setText(getattr(parsed_log, 'date', 'N/A'))
            self.log_detail_panel.val_time.setText(getattr(parsed_log, 'time', 'N/A'))
            self.log_detail_panel.val_timezone.setText(getattr(parsed_log, 'timezone', 'N/A'))
            self.log_detail_panel.val_status.setText(str(getattr(parsed_log, 'status', 'N/A')))
            self.log_detail_panel.val_method.setText(getattr(parsed_log, 'method', 'N/A'))
            self.log_detail_panel.val_resource.setText(getattr(parsed_log, 'resource', 'N/A'))
            self.log_detail_panel.val_size.setText(f"{getattr(parsed_log, 'size', '0')} Bytes")

    def next_page(self):
        """Flips forward one page chunk."""
        if self.log_manager.current_page < self.log_manager.total_pages() - 1:
            self.log_manager.current_page += 1
            self.display_current_page(self.log_manager.get_current_page_lines())
            self.update_navigation_buttons()

    def previous_page(self):
        """Flips backward one page chunk."""
        if self.log_manager.current_page > 0:
            self.log_manager.current_page -= 1
            self.display_current_page(self.log_manager.get_current_page_lines())
            self.update_navigation_buttons()

    def update_navigation_buttons(self):
        """Dynamically toggles gray out status based on dataset extremes."""
        curr = self.log_manager.current_page
        total = self.log_manager.total_pages()

        # Previous page is clickable only if we're past page 1
        self.bottom_bar.previous_btn.setEnabled(curr > 0)
        
        # Next page is clickable only if there's room to walk right
        self.bottom_bar.next_btn.setEnabled(curr < total - 1 and total > 0)
        
        # Update app title bar info to give active user tracking perspective
        if total > 0:
            self.setWindowTitle(f'Shrek log browser - Page {curr + 1} of {total} ({self.log_manager.total_count()} entries)')
        else:
            self.setWindowTitle('Shrek log browser - No file loaded')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())