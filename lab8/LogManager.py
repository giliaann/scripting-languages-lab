from pathlib import Path
from datetime import datetime, timezone
from utils import HTTPLog, parse_http_log

HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH']

class InvalidDateFormatError(ValueError):
    """Raised when a string does not match the YYYY-MM-DD format."""
    pass

class InvalidDateRangeError(ValueError):
    """Raised when the start date is later than the end date."""
    pass

class LogManager:
    def __init__(self, page_size):
        self._raw_lines: list[str] = []
        self.current_file_path: Path | None = None
        self.current_page = 0
        self.page_size = page_size
        
        # Instead of re-reading the file, we remember "bookmarks" (byte offsets) 
        # pointing to the start of each page within the file.
        self.page_offsets: list[int] = [0]
        
        # Time filter state
        self.start_date: datetime | None = None
        self.end_date: datetime | None = None

        # Method filter
        self.method_filter: str | None = None

    def _reset_pagination(self) -> None:
        """Resets cursor and bookmarks (used when changing file or filters)."""
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
        
    
    def set_dates_from_strings(self, start_date_str: str, end_date_str: str) -> list[str]:
        """Takes dates as YYYY-MM-DD strings, validates them, and sets the filter."""
        try:
            start_date = datetime.fromisoformat(start_date_str)
            end_date = datetime.fromisoformat(end_date_str)
        except ValueError:
            raise InvalidDateFormatError("Failed to parse dates. Required format is YYYY-MM-DD.")

        if start_date > end_date:
            raise InvalidDateRangeError("Start date cannot be later than the end date.")

        start_date = start_date.replace(tzinfo=timezone.utc)
        end_date = end_date.replace(hour=23, minute=59, second=59, tzinfo=timezone.utc)

        return self.set_dates(start_date, end_date)
    
    def set_method(self, method: str | None) -> list[str]:
        """Takes HTTP method, and sets the filter."""
        self.method_filter = method
        self._reset_pagination()

    def delete_dates(self) -> list[str]:
        """Removes the date filter, returning the manager to unrestricted mode."""
        self.start_date = None
        self.end_date = None
        self._reset_pagination()
   

    def _fetch_page(self, start_offset: int) -> tuple[list[str], int]:
        """
        Jumps to the specified byte in the file and reads exactly ONE page.
        Returns a list of loaded lines and the byte offset where reading finished.
        """
        lines = []
        next_offset = start_offset
        
        if not self.current_file_path or not self.current_file_path.exists():
            return lines, next_offset
            
        # NOTE: Using 'rb' to operate precisely on bytes. 
        # In text mode ('r'), f.tell() can be unstable in Python.
        with open(self.current_file_path, 'rb') as f:
            f.seek(start_offset)
            
            while len(lines) < self.page_size:
                line_bytes = f.readline()
                if not line_bytes:
                    break  # Actual end of file
                    
                # Save pointer after reading a line
                next_offset = f.tell()
                
                # Decode only for verification and parsing
                line_str = line_bytes.decode('utf-8', errors='replace').strip()
                if not line_str:
                    continue
                    
                # Apply time filters
                if self.start_date and self.end_date:
                    parsed_log = parse_http_log(line_str)
                    if not parsed_log or not (self.start_date <= parsed_log.datetime <= self.end_date):
                        continue

                if self.method_filter:
                    parsed_log = parse_http_log(line_str)
                    if not parsed_log or not (self.method_filter == parsed_log.method):
                        continue                
                        
                lines.append(line_str)
                
        return lines, next_offset


    # --- PAGINATION FUNCTIONS ---

    def load_first_page(self) -> list[str]:
        self.current_page = 0
        return self.load_current_page()

    def load_current_page(self) -> list[str]:
        if self.current_page >= len(self.page_offsets):
            return self._raw_lines
            
        # Get bookmark for the current page and start from there
        current_offset = self.page_offsets[self.current_page]
        lines, next_offset = self._fetch_page(current_offset)
        
        self._raw_lines = lines
        
        # Save bookmark for where the NEXT page begins
        if self.current_page + 1 == len(self.page_offsets):
            self.page_offsets.append(next_offset)
        else:
            self.page_offsets[self.current_page + 1] = next_offset
            
        return self._raw_lines

    def load_next_page(self) -> list[str]:
        """Advances the cursor and loads the next page using cached offsets."""
        # If we have a bookmark for the next page:
        if self.current_page + 1 < len(self.page_offsets):
            self.current_page += 1
            lines = self.load_current_page()
            
            # Prevent moving to an empty page
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


    # --- OTHER METHODS ---

    def get_current_page_lines(self) -> list[str]:
        return self._raw_lines
    
    def get_current_path_line_count(self) -> int:
        return len(self._raw_lines)
    
    def get_parsed_log_at(self, index_on_page: int) -> HTTPLog | None:
        if 0 <= index_on_page < len(self._raw_lines):
            raw_line = self._raw_lines[index_on_page]
            return parse_http_log(raw_line)
        return None