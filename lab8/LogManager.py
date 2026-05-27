import sqlite3
import pandas as pd
import re
from pathlib import Path


class LogDataManager:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.current_filtered_ids = []
        self.current_index = -1


    def load_file(self, file_path: Path):
        self.conn.execute("DROP TABLE IF EXISTS Logs")
        self.conn.execute("""

        """)