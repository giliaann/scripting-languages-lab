import sys
from datetime import datetime
from lab3.log_definition import LogField, LOG_SCHEMA
        
#cat lab3\http_first_100k.log | uv run python lab3\read_log.py 


def parse_http_log(data):
    return tuple(log_field.parser(val) for val, log_field in zip(data, LOG_SCHEMA))


def read_log():
    return [
        parse_http_log(log.strip().split('\t')) 
        for log in sys.stdin 
        if log.strip()
    ]


if __name__ == '__main__':
    logs = read_log()
    print(logs[:10])