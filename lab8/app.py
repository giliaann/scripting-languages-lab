import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, 
                               QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, 
                               QLineEdit, QListWidget)
from PySide6.QtCore import Qt


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
        self.log_list.addItems([
            '66.111.54.249 - - [22/Jan/2019:03:56:51 +0330] "GET /image/509...' for _ in range(20)
        ])
        layout.addWidget(self.log_list)


class LogDetailPanel(QWidget):
    """Handles the grid view of specific log details (right side)."""
    def __init__(self):
        super().__init__()
        layout = QGridLayout(self)

        # Row 0: remote host
        layout.addWidget(QLabel('Remote host'), 0, 0)
        self.val_remote_host = QLineEdit('66.111.54.249')
        layout.addWidget(self.val_remote_host, 0, 1)

        # Row 1: date
        layout.addWidget(QLabel('Date'), 1, 0)
        self.val_date = QLineEdit('2019-01-22')
        layout.addWidget(self.val_date, 1, 1, 1, 3) 

        # Row 2: time / timezone
        layout.addWidget(QLabel('Time'), 2, 0)
        self.val_time = QLineEdit('03:56:51')
        layout.addWidget(self.val_time, 2, 1)
        
        layout.addWidget(QLabel('Timezone:'), 2, 2)
        self.val_timezone = QLineEdit('Asia/Tehran')
        layout.addWidget(self.val_timezone, 2, 3)

        # Row 3: status code / method
        layout.addWidget(QLabel('Status code:'), 3, 0)
        
        self.val_status = QLabel('200')
        layout.addWidget(self.val_status, 3, 1)

        layout.addWidget(QLabel('Method:'), 3, 2)
        self.val_method = QLabel('GET')
        layout.addWidget(self.val_method, 3, 3)

        # Row 4: resource
        layout.addWidget(QLabel('Resource:'), 4, 0)
        self.val_resource = QLineEdit('/image/50995/productModel/200x200')
        layout.addWidget(self.val_resource, 4, 1, 1, 3)

        # Row 5: size
        layout.addWidget(QLabel('Size:'), 5, 0)
        self.val_size = QLabel('2244 Bytes')
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())