import sys
from LogType import LogType


def read_log() -> list[LogType]:
    logs_list = []

    for line in sys.stdin:
        line = line.strip()

        # skip empty lines
        if not line:
            continue

        sep = '\t'
        tokens = line.split(sep)

        # 0 - timestamp (datetime)
        ts = datetime.fromtimestamp(float(tokens[0]))
        # 1 - uid (string)
        uid = tokens[1]
        # 2 - source ip (string)
        src_ip = tokens[2]
        # 3 - source port (int)
        src_port = int(tokens[3])
        # 4 - destination ip (string)
        dest_ip = tokens[4]
        # 5 - destiatnion port (int)
        dest_port = int(tokens[5])
        # 6 - HTTP method (string)
        http_method = tokens[6]
        # 7 - host name - destiatnion -  name (? ip) (string)
        host_name = tokens[7]
        # 8 - uri, resource path - (string)
        path = tokens[8]
        # 14 - status code (int)
        status_code = int(tokens[14]) if tokens[14] != '-' else None
        # 15 - status msg (string)
        status_msg = tokens[15] if tokens[15] != '-' else None

        #None
        logs_list.append((ts, uid, src_ip, src_port, dest_ip, dest_port, http_method, host_name, path, status_code, status_msg))

    return logs_list
        
#cat lab3\http_first_100k.log | uv run python lab3\read_log.py 