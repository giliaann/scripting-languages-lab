from PySide6.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Hello world app')


        menubar = self.menuBar()

        fileMenu = menubar.addMenu('File')
        editMenu = menubar.addMenu('Edit')
        helpMenu = menubar.addMenu('?')

        aboutAction = helpMenu.addAction('About')

        submenu = fileMenu.addMenu('Submenu')
        exitAction = submenu.addAction('Exit')

        exitAction.triggered.connect(self.close)
        aboutAction.triggered.connect(lambda: print('This is a tutorial GUI APP'))



app = QApplication()
window = MainWindow()
window.show()

app.exec()