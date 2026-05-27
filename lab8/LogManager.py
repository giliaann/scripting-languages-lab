from pathlib import Path
from dataclasses import dataclass
from datetime import datetime
import re

from utils import HTTPLog, parse_http_log


class LogManager:
    def __init__(self):
        self._raw_lines = list[str] = []
        self.current_file_path: Path | None = None

    
    def load_file(self, file_path: Path) -> list[str]:
        self.current_file_path = file_path
        self._raw_lines = []

        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                cleaned = line.strip()
                if cleaned:
                    self._raw_lines.append(cleaned)

        return self._raw_lines
    

    def get_parsed_log_at(self, index: int) -> HTTPLog | None:
        if 0 <= index <= len(self._raw_lines):
            raw_line = self._raw_lines[index]
            return parse_http_log(raw_line)
        return None
    

    def total_count(self) -> int:
        return len(self._raw_lines)