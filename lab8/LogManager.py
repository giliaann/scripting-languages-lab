from pathlib import Path
from utils import HTTPLog, parse_http_log


class LogManager:
    def __init__(self, page_size):
        self._raw_lines: list[str] = []
        self.current_file_path: Path | None = None
        self.current_page = 0
        self.page_size = page_size
        self.logs_count = 0
        self.pages_count = 0

    
    def load_file(self, file_path: Path) -> list[str]:
        """Loads file and returns the raw text from the first page"""
        self.current_file_path = file_path
        self.current_page = 0
        self.logs_count = self.get_logs_count()
        self.pages_count = (self.logs_count + self.page_size - 1) // self.page_size
        return self.load_page(page_num = 0)
    

    def get_logs_count(self) -> int:
        if not self.current_file_path or not self.current_file_path.exists():
            return 0
        
        try:
            with open(self.current_file_path, 'rb') as f:
                line_count = sum(1 for _ in f)

            return line_count
        except Exception:
            return 0


    def load_page(self, page_num: int):
        """Loads a page at given index into _raw_lines and returns it"""
        if not self.current_file_path or not self.current_file_path.exists():
            return []
        
        self.current_page = page_num
        self._raw_lines = []

        start_line_index = self.current_page * self.page_size

        try:
            with open(self.current_file_path, 'r', encoding='utf-8', errors='replace') as f:
                # Przeskakujemy linie z poprzednich stron
                for _ in range(start_line_index):
                    if not f.readline():
                        return []
                    
                # POPRAWKA 2: Czytamy dopóki nie uzbieramy pełnej strony niepustych linii
                while len(self._raw_lines) < self.page_size:
                    line = f.readline()
                    if not line:
                        break  # Koniec pliku

                    cleaned = line.strip()
                    if cleaned:
                        self._raw_lines.append(cleaned)

        except OSError:
            return []
        
        return self._raw_lines
    

    def get_current_page_lines(self) -> list[str]:
        return self._raw_lines
    

    def get_current_path_line_count(self) -> int:
        return len(self._raw_lines)
    

    def get_parsed_log_at(self, index_on_page: int) -> HTTPLog | None:
        # POPRAWKA 1: Zamiana '<=' na '<' chroni przed IndexError
        if 0 <= index_on_page < len(self._raw_lines):
            raw_line = self._raw_lines[index_on_page]
            return parse_http_log(raw_line)
        return None