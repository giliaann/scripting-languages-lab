import re
from dataclasses import dataclass
from datetime import datetime

@dataclass(slots=True)
class HTTPLog:
    remote_host: str  # ZMIANA: Zmień z 'ip' na 'remote_host', aby pasowało do GUI
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
    r'(?P<remote_host>\S+) '           # ZMIANA: Grupa nazywa się teraz <remote_host>
    r'\S+ \S+ '                         # Ignorujemy tożsamość i user-id
    r'\[(?P<datetime>[^\]]+)\] '        # Data i czas
    r'"(?P<method>[A-Z]+) '             # Metoda
    r'(?P<resource>\S+) '               # Zasób (URL)
    r'\S+" '                            # Ignorujemy wersję protokołu
    r'(?P<status>\d{3}) '               # Status kod
    r'(?P<size>\d+|-)'                  # Rozmiar bajtów
)


def parse_http_log(line: str) -> HTTPLog:
    match = LOG_PATTERN.match(line)
    if not match:
        return None
    
    parsed_data = match.groupdict()
    # Teraz parsed_data zawiera klucz 'remote_host', który idealnie wstrzykuje się do HTTPLog
    log_entry = HTTPLog(**parsed_data)
    return log_entry