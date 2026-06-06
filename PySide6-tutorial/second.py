import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QGridLayout, QHBoxLayout
)
from PySide6.QtCore import Qt

class LogDetailsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Log Entry Viewer")
        self.resize(550, 400)
        
        # Main Window Styling (Using a casual font to match the image vibe)
        self.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
                font-size: 16px;
                color: #000000;
            }
            QLabel {
                font-weight: bold;
            }
        """)

        # Shared style for the rectangular value boxes
        box_style = """
            border: 2px solid #000000;
            padding: 6px 12px;
            background-color: #FFFFFF;
            font-weight: bold;
        """

        # Main Layout
        grid = QGridLayout()
        grid.setSpacing(15)
        grid.setContentsMargins(30, 30, 30, 30)

        # --- Row 0: Remote Host ---
        lbl_remote = QLabel("Remote host")
        val_remote = QLabel("66.111.54.249")
        val_remote.setStyleSheet(box_style)
        val_remote.setFixedWidth(180)
        
        grid.addWidget(lbl_remote, 0, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        grid.addWidget(val_remote, 0, 1, Qt.AlignmentFlag.AlignLeft)

        # --- Row 1: Date ---
        lbl_date = QLabel("Date")
        val_date = QLabel("2019-01-22")
        val_date.setStyleSheet(box_style)
        val_date.setMinimumWidth(350)
        
        grid.addWidget(lbl_date, 1, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        grid.addWidget(val_date, 1, 1, Qt.AlignmentFlag.AlignLeft)

        # --- Row 2: Time & Timezone (Inline) ---
        lbl_time = QLabel("Time")
        
        val_time = QLabel("03:56:51")
        val_time.setStyleSheet(box_style)
        val_time.setFixedWidth(130)
        
        lbl_tz = QLabel("Timezone:")
        
        val_tz = QLabel("Asia/Tehran")
        val_tz.setStyleSheet(box_style)
        val_tz.setFixedWidth(130)

        time_layout = QHBoxLayout()
        time_layout.addWidget(val_time)
        time_layout.addWidget(lbl_tz)
        time_layout.addWidget(val_tz)
        time_layout.addStretch()
        time_layout.setSpacing(15)
        
        grid.addWidget(lbl_time, 2, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        grid.addLayout(time_layout, 2, 1)

        # --- Row 3: Status Code & Method (Inline) ---
        lbl_status = QLabel("Status code:")
        
        # Perfect Green Circle via QSS
        val_status = QLabel("200")
        val_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        val_status.setStyleSheet("""
            background-color: #39FF14;
            border: 2px solid #20C20A;
            border-radius: 25px;
            min-width: 50px;
            max-width: 50px;
            min-height: 50px;
            max-height: 50px;
            font-weight: bold;
            font-size: 15px;
        """)
        
        lbl_method = QLabel("Method:")
        val_method = QLabel("GET")
        
        status_layout = QHBoxLayout()
        status_layout.addWidget(val_status)
        status_layout.addWidget(lbl_method)
        status_layout.addWidget(val_method)
        status_layout.addStretch()
        status_layout.setSpacing(20)

        grid.addWidget(lbl_status, 3, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        grid.addLayout(status_layout, 3, 1)

        # --- Row 4: Resource ---
        lbl_resource = QLabel("Resource:")
        val_resource = QLabel("/image/50995/productModel/200x200")
        val_resource.setStyleSheet(box_style)
        val_resource.setMinimumWidth(380)
        
        grid.addWidget(lbl_resource, 4, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        grid.addWidget(val_resource, 4, 1, Qt.AlignmentFlag.AlignLeft)

        # --- Row 5: Size ---
        lbl_size = QLabel("Size:")
        val_size = QLabel("2244 Bytes")
        
        grid.addWidget(lbl_size, 5, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        grid.addWidget(val_size, 5, 1, Qt.AlignmentFlag.AlignLeft)

        # Prevent components from expanding vertically
        grid.setRowStretch(6, 1) 
        self.setLayout(grid)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogDetailsWidget()
    window.show()
    sys.exit(app.exec())