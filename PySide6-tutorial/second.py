from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Hello world app')

        button = QPushButton('Show choices')
        button.clicked.connect(self.ask_choices)
        self.setCentralWidget(button)


    def ask_yes_no(self):
        if QMessageBox.question(self,'Question', 'DO you like python?') == QMessageBox.Yes:
            print('user likes python')
        else:
            print('User does not like python')


    def ask_choices(self):
        msg = QMessageBox(self)
        msg.setWindowTitle('CHoice')
        msg.setText('Select your favourite programming language')
        python = msg.addButton('Python', QMessageBox.AcceptRole)
        cpp = msg.addButton('Cpp', QMessageBox.AcceptRole)
        java = msg.addButton('Java', QMessageBox.AcceptRole)

        msg.exec()

        if msg.clickedButton() == python:
            print('Users favourite language is python')
        elif msg.clickedButton() == cpp:
            print('its c++')
        else:
            print('its java :()')


app = QApplication()
window = MainWindow()
window.show()

app.exec()


