import sys
from datetime import datetime
        
#cat lab3\http_first_100k.log | uv run python lab3\read_log.py 


def parse_http_log(data):
    cast_funcs = (lambda x : datetime.fromtimestamp(float(x)), str, str, int, str, int, int, str, str, str, str, str, int, int, float, str, float, str, float, str, str, float, str, str, str, str, str)

    return tuple(
        cast_func(val) if val != '-' else None
        for val, cast_func in zip(data, cast_funcs)
    )


def read_log():
    return [
        parse_http_log(log.strip().split('\t')) 
        for log in sys.stdin 
        if log.strip()
    ]


if __name__ == '__main__':
    logs = read_log()
    for log in logs[:10]:
        print(log)