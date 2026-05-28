import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, 
                               QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, 
                               QLineEdit, QListWidget, QMessageBox)
from PySide6.QtCore import Qt

from LogManager import LogManager, InvalidDateFormatError, InvalidDateRangeError
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
        self.from_date_text = QLineEdit('YYYY-MM-DD')
        from_date_layout.addWidget(self.from_label)
        from_date_layout.addWidget(self.from_date_text)
        filter_date_layout.addLayout(from_date_layout)

        to_date_layout = QHBoxLayout()
        self.to_label = QLabel('To')
        self.to_date_text = QLineEdit('YYYY-MM-DD')
        to_date_layout.addWidget(self.to_label)
        to_date_layout.addWidget(self.to_date_text)
        filter_date_layout.addLayout(to_date_layout)

        self.filter_btn = QPushButton('Apply filter')
        self.filter_btn.setCheckable(True)
        filter_date_layout.addWidget(self.filter_btn)
        
        layout.addLayout(filter_date_layout)

        # Log List
        self.log_list = QListWidget()
        self.log_list.setTextElideMode(Qt.TextElideMode.ElideRight)
        self.log_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        layout.addWidget(self.log_list)

        # Page change buttons
        page_btn_layout = QHBoxLayout()
        self.prev_page_btn = QPushButton('Previous page')
        self.next_page_btn = QPushButton('Next page')
        
        # Current page number label
        self.page_label = QLabel('Page: -')
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layout
        page_btn_layout.addWidget(self.prev_page_btn)
        page_btn_layout.addStretch()
        
        page_btn_layout.addWidget(self.page_label)
        
        page_btn_layout.addStretch()
        page_btn_layout.addWidget(self.next_page_btn)
        layout.addLayout(page_btn_layout)


class LogDetailPanel(QWidget):
    """Handles the grid view of specific log details (right side)."""
    def __init__(self):
        super().__init__()
        layout = QGridLayout(self)

        # Row 0
        layout.addWidget(QLabel('Remote host'), 0, 0)
        self.val_remote_host = QLineEdit('-')
        self.val_remote_host.setReadOnly(True)
        layout.addWidget(self.val_remote_host, 0, 1, 1, 3)

        # Row 1
        layout.addWidget(QLabel('Date'), 1, 0)
        self.val_date = QLineEdit('-')
        self.val_date.setReadOnly(True)
        layout.addWidget(self.val_date, 1, 1, 1, 3) 

        # Row 2
        layout.addWidget(QLabel('Time'), 2, 0)
        self.val_time = QLineEdit('-')
        self.val_time.setReadOnly(True)
        layout.addWidget(self.val_time, 2, 1)
        
        layout.addWidget(QLabel('Timezone:'), 2, 2)
        self.val_timezone = QLineEdit('-')
        self.val_timezone.setReadOnly(True)
        layout.addWidget(self.val_timezone, 2, 3)

        # Row 3
        layout.addWidget(QLabel('Status code:'), 3, 0)
        self.val_status = QLabel('-')
        layout.addWidget(self.val_status, 3, 1)

        layout.addWidget(QLabel('Method:'), 3, 2)
        self.val_method = QLabel('-')
        layout.addWidget(self.val_method, 3, 3)

        # Row 4
        layout.addWidget(QLabel('Resource:'), 4, 0)
        self.val_resource = QLineEdit('-')
        self.val_resource.setReadOnly(True)
        layout.addWidget(self.val_resource, 4, 1, 1, 3)

        # Row 5
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

        # Functionalities
        self.log_manager = LogManager(page_size=1000)

        self.top_bar.open_btn.clicked.connect(self.load_file_clicked)
        self.log_list_panel.log_list.currentRowChanged.connect(self.log_selection_changed)
        
        self.bottom_bar.next_btn.clicked.connect(self.next_log)
        self.bottom_bar.previous_btn.clicked.connect(self.previous_log)
        
        self.log_list_panel.next_page_btn.clicked.connect(self.next_page)
        self.log_list_panel.prev_page_btn.clicked.connect(self.previous_page)
        
        self.log_list_panel.filter_btn.clicked.connect(self.apply_remove_filter)

        # Disable buttons on startup
        self.update_log_nav_btn()
        self.update_page_nav_btn()

    def _update_list_and_ui(self, raw_lines: list[str]):
        """Helper method to populate the UI with a given list of strings and refresh buttons."""
        self.log_list_panel.log_list.clear()
        
        if raw_lines:
            self.log_list_panel.log_list.addItems(raw_lines)
            self.log_list_panel.log_list.setCurrentRow(0)
            
        self.update_log_nav_btn()
        self.update_page_nav_btn()

    def load_file_clicked(self):
        path_str = self.top_bar.path_input.text().strip()
        if not path_str:
            QMessageBox.warning(self, 'Missing path', 'Please provide a path to the log file before clicking Open.')
            return
        
        path = Path(path_str)

        try:
            raw_lines = self.log_manager.load_file(path)
            if not raw_lines:
                QMessageBox.information(self, 'Empty file', 'The selected file does not contain logs or is empty.')
            
            self._update_list_and_ui(raw_lines)

        except FileNotFoundError:
            QMessageBox.critical(self, 'Error: Not found', f'File path: {path} does not exist.')
        except PermissionError:
            QMessageBox.critical(self, 'Error: Permission denied', f'You do not have permission to open file {path}.')
        except IsADirectoryError:
            QMessageBox.critical(self, 'Error: Path is a directory', f'The provided path: {path} is a directory, not a file.')
        except Exception as e:
            QMessageBox.critical(self, 'Critical error', f'Unexpected error while loading the file:\n{str(e)}')

    def apply_remove_filter(self, checked):
            if checked:
                self.log_list_panel.from_date_text.setReadOnly(True)
                self.log_list_panel.to_date_text.setReadOnly(True)
                
                start_str = self.log_list_panel.from_date_text.text().strip()
                end_str = self.log_list_panel.to_date_text.text().strip()
                
                try:
                    raw_lines = self.log_manager.set_dates_from_strings(start_str, end_str)
                    self.log_list_panel.filter_btn.setText('Remove filter')
                    self._update_list_and_ui(raw_lines)
                except (InvalidDateFormatError, InvalidDateRangeError, Exception) as e:
                    self.log_list_panel.filter_btn.setChecked(False)
                    self.log_list_panel.from_date_text.setReadOnly(False)
                    self.log_list_panel.to_date_text.setReadOnly(False)
                    
                    if isinstance(e, InvalidDateFormatError):
                        QMessageBox.critical(self, "Format error", str(e))
                    elif isinstance(e, InvalidDateRangeError):
                        QMessageBox.critical(self, "Date range error", str(e))
                    else:
                        QMessageBox.critical(self, "Unexpected error", str(e))
            else:
                self.log_list_panel.from_date_text.setReadOnly(False)
                self.log_list_panel.to_date_text.setReadOnly(False)
                
                raw_lines = self.log_manager.delete_dates()
                self.log_list_panel.filter_btn.setText('Apply filter')
                self._update_list_and_ui(raw_lines)

    def log_selection_changed(self, index: int):
        if index < 0:
            self.clear_log_details()
            self.update_log_nav_btn()
            return

        self.update_log_nav_btn()
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

    def next_log(self):
        current_row = self.log_list_panel.log_list.currentRow()
        if current_row < self.log_list_panel.log_list.count() - 1:
            self.log_list_panel.log_list.setCurrentRow(current_row + 1)

    def previous_log(self):
        current_row = self.log_list_panel.log_list.currentRow()
        if current_row > 0:
            self.log_list_panel.log_list.setCurrentRow(current_row - 1)

    def next_page(self):
        raw_lines = self.log_manager.load_next_page()
        self._update_list_and_ui(raw_lines)

    def previous_page(self):
        raw_lines = self.log_manager.load_prev_page()
        self._update_list_and_ui(raw_lines)

    def update_log_nav_btn(self):
        curr = self.log_list_panel.log_list.currentRow()
        total = self.log_list_panel.log_list.count()
        self.bottom_bar.previous_btn.setEnabled(curr > 0)
        self.bottom_bar.next_btn.setEnabled(curr < total - 1 and total > 0)

    def update_page_nav_btn(self):
            curr = self.log_manager.current_page
            
            lines_count = len(self.log_manager.get_current_page_lines())
            has_logs = lines_count > 0
            
            # Assuming that if the page is not "full", it is the last page
            is_full_page = lines_count == self.log_manager.page_size
            
            self.log_list_panel.prev_page_btn.setEnabled(curr > 0)
            self.log_list_panel.next_page_btn.setEnabled(is_full_page)
            
            if has_logs:
                self.log_list_panel.page_label.setText(f"Page: {curr + 1}")
                self.setWindowTitle(f'Shrek log browser - Page {curr + 1}')
            else:
                self.log_list_panel.page_label.setText("Page: -")
                self.setWindowTitle('Shrek log browser - No logs found')
    
    def clear_log_details(self):
        """Clears the right panel with log details."""
        self.log_detail_panel.val_remote_host.setText('-')
        self.log_detail_panel.val_date.setText('-')
        self.log_detail_panel.val_time.setText('-')
        self.log_detail_panel.val_timezone.setText('-')
        self.log_detail_panel.val_status.setText('-')
        self.log_detail_panel.val_method.setText('-')
        self.log_detail_panel.val_resource.setText('-')
        self.log_detail_panel.val_size.setText('- Bytes')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())