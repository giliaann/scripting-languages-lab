import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My first PySide App")
        self.resize(300, 200)

        self.label = QLabel("Click the button below", self)
        self.button = QPushButton("Click me", self)

        self.button.clicked.connect(self.on_button_click)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    
    def on_button_click(self):
        self.label.setText("Ouch!")
        self.button.setText("CLicked")
        self.button.setEnabled(True)



if __name__=='__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())