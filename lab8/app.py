import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QListWidget, QFormLayout)
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Shrek log browser')

        container = QWidget()
        self.setCentralWidget(container)

        # main layout
        layout = QVBoxLayout(container)
        # top layout
        top_layout = QHBoxLayout()
        self.path_input = QLineEdit('Input path to log file')
        self.open_btn = QPushButton('Open')
        top_layout.addWidget(self.path_input)
        top_layout.addWidget(self.open_btn)
        layout.addLayout(top_layout)

        # middle layout
        mid_layout = QHBoxLayout()
        # middle left layout
        log_display_layout = QVBoxLayout()
        # filter date part
        filter_date_layout = QHBoxLayout()

        from_date_layout = QHBoxLayout()
        self.from_label = QLabel('From')
        self.from_date_text = QLineEdit('2019-10-12')
        from_date_layout.addWidget(self.from_label)
        from_date_layout.addWidget(self.from_date_text)
        filter_date_layout.addLayout(from_date_layout)

        to_date_layout = QHBoxLayout()
        self.to_label = QLabel('To')
        self.to_date_text = QLineEdit('2020-09-05')
        to_date_layout.addWidget(self.to_label)
        to_date_layout.addWidget(self.to_date_text)
        filter_date_layout.addLayout(to_date_layout)

        log_display_layout.addLayout(filter_date_layout)

        # log list
        self.log_list = QListWidget()
        self.log_list.addItems(['Log1', 'Log2', 'Log3'])
        log_display_layout.addWidget(self.log_list)

        mid_layout.addLayout(log_display_layout)

        # right layout
        detail_display_layout = QVBoxLayout()

        mid_layout.addLayout(detail_display_layout)

        layout.addLayout(mid_layout)


        # bottom layout
        bottom_layout = QHBoxLayout()
        self.previous_btn = QPushButton('Previous')
        self.next_btn = QPushButton('Next')
        bottom_layout.addWidget(self.previous_btn)
        bottom_layout.addWidget(self.next_btn)
        layout.addLayout(bottom_layout)


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()