from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QPushButton, QLineEdit, 
                               QTextEdit, QSlider, QProgressBar, QComboBox, QListWidget, QRadioButton, QCheckBox,
                               QHBoxLayout)

from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Hello World Application')

        container = QWidget()
        self.setCentralWidget(container)

        layout = QVBoxLayout(container)

        label = QLabel('Label')
        label.setAlignment(Qt.AlignCenter)

        button = QPushButton('CLick me')
        button.clicked.connect(lambda: print('Button clicked'))

        listwidget = QListWidget()
        listwidget.addItems(['ONe', 'Two', 'Three'])

        listwidget.itemClicked.connect(lambda item: print(f'Item clicked {item.text()}'))
        listwidget.itemDoubleClicked.connect(lambda item: print(f'Item doubleclicked {item.text()}'))

        inner_container = QWidget()

        inner_layout = QHBoxLayout(inner_container)

        radio1 = QRadioButton('One')
        radio2 = QRadioButton('Two')
        radio3 = QRadioButton('Three')

        for r in (radio1, radio2, radio3):
            r.toggled.connect(self.radio_changed)

        inner_layout.addWidget(radio1)
        inner_layout.addWidget(radio2)
        inner_layout.addWidget(radio3)

        layout.addWidget(label)
        layout.addWidget(button)
        layout.addWidget(listwidget)
        layout.addWidget(inner_container)


    def radio_changed(self):
        r = self.sender()
        if r.isChecked():
            print('Radio button was selected! Value', r.text())


app = QApplication()
window = MainWindow()
window.show()

app.exec()


