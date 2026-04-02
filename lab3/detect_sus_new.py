from lab3.log_definition import get_index
from collections import defaultdict
from datetime import timedelta

status_code_index = get_index('status_code')


def calc_fast_requests(entries):
    ts_index = get_index('ts')
    count = 0

    if not entries:
        return 0
    
    prev = entries[0]
    for entry in sorted(entries, key = lambda entry : entry[ts_index])[1:]:
        if (entry[ts_index] - prev[ts_index]) < timedelta(seconds=1):
            count += 1
        prev = entry
    return count


def detect_sus(log, threshold, weights = (1.0, 2.0, 0.5)):
    w1, w2, w3 = weights
    id_orig_h_index = get_index('id_orig_h')
    ip_to_entries = defaultdict(list)
    for entry in log:
        ip_orig_h = entry[id_orig_h_index]
        ip_to_entries[ip_orig_h].append(entry)

    result = {}
    for ip, entries in ip_to_entries.items():
        requests_count = len(entries)
        errors_404_count = sum(1 for entry in entries if entry[status_code_index] == 404)
        fast_requests_count = calc_fast_requests(entries)
        score = w1 * requests_count + w2 * errors_404_count + w3 * fast_requests_count
        if score > threshold:
            result[f"{ip}"] = {
            "requests" : requests_count,
            "errors_404" : errors_404_count,
            "score" : score
        }
            
    return result


from lab3.read_log import read_log
import pprint

if __name__ == '__main__':
    logs = read_log()
    pprint.pprint(detect_sus(logs, 300))