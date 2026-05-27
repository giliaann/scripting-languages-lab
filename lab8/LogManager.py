from pathlib import Path
from datetime import datetime, timezone
from utils import HTTPLog, parse_http_log

class InvalidDateFormatError(ValueError):
    """Rzucany, gdy string nie pasuje do formatu YYYY-MM-DD."""
    pass

class InvalidDateRangeError(ValueError):
    """Rzucany, gdy data początkowa jest późniejsza niż końcowa."""
    pass

class LogManager:
    def __init__(self, page_size):
        self._raw_lines: list[str] = []
        self.current_file_path: Path | None = None
        self.current_page = 0
        self.page_size = page_size
        
        # Zamiast czytać plik od nowa, zapamiętujemy "zakładki" (byte offsets) 
        # wskazujące na początek każdej strony wewnątrz pliku.
        self.page_offsets: list[int] = [0]
        
        # Stan filtra czasowego
        self.start_date: datetime | None = None
        self.end_date: datetime | None = None

    def _reset_pagination(self) -> None:
        """Resetuje kursor i zakładki (używane przy zmianie pliku lub filtrów)."""
        self.current_page = 0
        self.page_offsets = [0]
        self._raw_lines = []
    
    def load_file(self, file_path: Path) -> list[str]:
        """Loads file and returns the raw text from the first page."""
        self.current_file_path = file_path
        self._reset_pagination()
        return self.load_current_page()

    def set_dates(self, start_date: datetime, end_date: datetime) -> list[str]:
        """Sets the date range filter and resets the cursor to the first page."""
        self.start_date = start_date
        self.end_date = end_date
        self._reset_pagination()
        return self.load_current_page()
    
    def set_dates_from_strings(self, start_date_str: str, end_date_str: str) -> list[str]:
        """
        Przyjmuje daty jako stringi YYYY-MM-DD, waliduje je i ustawia filtr.
        """
        try:
            start_date = datetime.fromisoformat(start_date_str)
            end_date = datetime.fromisoformat(end_date_str)
        except ValueError:
            raise InvalidDateFormatError(f"Nie udało się przeparsować dat. Wymagany format to YYYY-MM-DD.")

        if start_date > end_date:
            raise InvalidDateRangeError("Data początkowa (start) nie może być późniejsza niż data końcowa (finish).")

        start_date = start_date.replace(tzinfo=timezone.utc)
        end_date = end_date.replace(hour=23, minute=59, second=59, tzinfo=timezone.utc)

        # Na koniec używamy poprzednio stworzonej metody, aby zastosować filtry i zresetować kursor
        return self.set_dates(start_date, end_date)

    def delete_dates(self) -> list[str]:
        """Removes the date filter, returning the manager to unrestricted mode."""
        self.start_date = None
        self.end_date = None
        self._reset_pagination()
        return self.load_current_page()

    def _fetch_page(self, start_offset: int) -> tuple[list[str], int]:
        """
        Skacze do wskazanego bajtu w pliku i czyta dokładnie JEDNĄ stronę.
        Zwraca listę załadowanych linii oraz offset bajtowy, na którym skończono czytanie.
        """
        lines = []
        next_offset = start_offset
        
        if not self.current_file_path or not self.current_file_path.exists():
            return lines, next_offset
            
        # UWAGA: Używamy 'rb', aby precyzyjnie operować na bajtach.
        # W trybie tekstowym ('r') f.tell() może zachowywać się niestabilnie w Pythonie.
        with open(self.current_file_path, 'rb') as f:
            f.seek(start_offset)
            
            while len(lines) < self.page_size:
                line_bytes = f.readline()
                if not line_bytes:
                    break  # Prawdziwy koniec pliku
                    
                # Zapisujemy wskaźnik po przeczytaniu linii
                next_offset = f.tell()
                
                # Dekodujemy tylko w celu weryfikacji i parsowania
                line_str = line_bytes.decode('utf-8', errors='replace').strip()
                if not line_str:
                    continue
                    
                # Aplikacja filtrów czasowych
                if self.start_date and self.end_date:
                    parsed_log = parse_http_log(line_str)
                    if not parsed_log or not (self.start_date <= parsed_log.datetime <= self.end_date):
                        continue
                        
                lines.append(line_str)
                
        return lines, next_offset


    # --- 4 FUNKCJE STRONICOWANIA ---

    def load_first_page(self) -> list[str]:
        self.current_page = 0
        return self.load_current_page()

    def load_current_page(self) -> list[str]:
        if self.current_page >= len(self.page_offsets):
            return self._raw_lines
            
        # Pobieramy zakładkę dla bieżącej strony i ruszamy od niej
        current_offset = self.page_offsets[self.current_page]
        lines, next_offset = self._fetch_page(current_offset)
        
        self._raw_lines = lines
        
        # Zapisujemy zakładkę na przyszłość, gdzie zaczyna się NASTĘPNA strona
        if self.current_page + 1 == len(self.page_offsets):
            self.page_offsets.append(next_offset)
        else:
            self.page_offsets[self.current_page + 1] = next_offset
            
        return self._raw_lines

    def load_next_page(self) -> list[str]:
        """Advances the cursor and loads the next page using cached offsets."""
        # Jeżeli posiadamy zakładkę następnej strony (wygenerowaną przy czytaniu obecnej):
        if self.current_page + 1 < len(self.page_offsets):
            self.current_page += 1
            lines = self.load_current_page()
            
            # Zabezpieczenie przed przejściem na całkowicie pustą stronę
            if not lines and self.current_page > 0:
                self.current_page -= 1
                self.load_current_page()
                
        return self._raw_lines

    def load_prev_page(self) -> list[str]:
        """Moves the cursor back and loads the previous page."""
        if self.current_page > 0:
            self.current_page -= 1
            self.load_current_page()
        return self._raw_lines


    # --- POZOSTAŁE METODY ---

    def get_current_page_lines(self) -> list[str]:
        return self._raw_lines
    
    def get_current_path_line_count(self) -> int:
        return len(self._raw_lines)
    
    def get_parsed_log_at(self, index_on_page: int) -> HTTPLog | None:
        if 0 <= index_on_page < len(self._raw_lines):
            raw_line = self._raw_lines[index_on_page]
            return parse_http_log(raw_line)
        return None
    
