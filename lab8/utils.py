import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import itertools

@dataclass(slots=True)
class HTTPLog:
    ip: str
    datetime: datetime
    method: str
    resource: str
    status: str
    size: str


    def __post_init__(self):
        if isinstance(self.datetime, str):
            self.datetime = datetime.strptime(self.datetime, '%d/%b/%Y:%H:%M:%S %z')

    @property
    def date_only(self) -> str:
        return self.datetime.strftime('%Y-%m-%d')
    
    @property
    def time_only(self) -> str:
        return self.datetime.strftime('%H:%M:%S')
    

    @property
    def timezone(self) -> str:
        return self.datetime.strftime('%z')
    


LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) '                     # IP: ciąg znaków bez spacji
    r'\S+ \S+ '                         # Ignorujemy tożsamość i user-id (zazwyczaj "- -")
    r'\[(?P<datetime>[^\]]+)\] '        # Data i czas: wszystko wewnątrz nawiasów kwadratowych
    r'"(?P<method>[A-Z]+) '             # Metoda: wielkie litery na początku cudzysłowu (np. GET)
    r'(?P<resource>\S+) '               # Zasób (URL): ciąg znaków do spacji
    r'\S+" '                            # Ignorujemy wersję protokołu (np. HTTP/1.1)
    r'(?P<status>\d{3}) '               # Status kod: dokładnie 3 cyfry
    r'(?P<size>\d+|-)'                  # Rozmiar bajtów: cyfry lub myślnik (gdy brak)
)



def parse_http_log(line: str) -> HTTPLog:
    match = LOG_PATTERN.match(line)
    if not match:
        return None
    
    parsed_data = match.groupdict()
    log_entry = HTTPLog(**parsed_data)
    return log_entry

