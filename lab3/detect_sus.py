from lab3.log_definition import get_index
from collections import defaultdict

# jesli ilosc zapytan jest wieksza niz 20% thresholdu, to wtedy rozwazam czy to bot
# jesli sredni odstep czasu pomiedzy zapytaniami wynosi mniej niż sekunde to flaguje jako bota
# jesli wartosc zapytan jest wiesza niz threshold, to flaguje jako bota
# jesli wartosc bledow 404 jest wieksza niz 50% tresholdu to flaguje jako bota

# posegregowac zapytania do slownika mapujacego zapytania do adresow ip


def check_if_sus(entries, threshold):
    RATIO_OF_SUS = 0.2
    REQUEST_PER_SECOND_THRESHOLD = 100.0
    
    STATUS_CODE_404_THRESHOLD_RATIO = 0.5
    ts_index = get_index('ts')
    status_code_index = get_index('status_code')

    length = len(entries)
    
    if length < threshold * RATIO_OF_SUS:
        return False

    if length > threshold:
        return True

    first = min(entries, key = lambda entry : entry[ts_index])[ts_index]
    last = max(entries, key = lambda entry : entry[ts_index])[ts_index]
    delta = abs(last - first)

    if length / delta > REQUEST_PER_SECOND_THRESHOLD:
        return True
        
    count_404 = sum(1 for entry in entries if entry[status_code_index] == 404)
    if count_404 / length > STATUS_CODE_404_THRESHOLD_RATIO:
        return True
    
    return False


def detect_sus(log, threshold):
    id_orig_h_index = get_index('id_orig_h')
    ip_to_entries = defaultdict(list)
    for entry in log:
        ip_orig_h = entry[id_orig_h_index]
        ip_to_entries[ip_orig_h].append(entry)

    return [
        ip 
        for ip, entries in ip_to_entries.items() 
        if check_if_sus(entries, threshold)
    ]
    

from lab3.read_log import read_log
import pprint

if __name__ == '__main__':
    logs = read_log()
    THRESHOLD = 50_000
    pprint.pprint(
        detect_sus(logs, THRESHOLD)
    )
    