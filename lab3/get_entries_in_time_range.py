from lab3.log_definition import get_index
from lab3.read_log import read_log
from datetime import datetime

def get_entries_in_time_range(logs, start, end):
    ts_index = get_index('ts')
    return [log for log in logs if log[ts_index] and start <= log[ts_index] < end]

if __name__ == '__main__':
    ts_index = get_index('ts')
    logs = read_log()

    start = datetime(2012, 3, 16, 14, 0)
    end = datetime(2012, 3, 16, 14, 40)

    filtered_logs = get_entries_in_time_range(logs, start, end)
    for log in filtered_logs[:10]:
        print(log[ts_index])