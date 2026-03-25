from lab3.log_definition import get_index
from collections import Counter


def get_counts(field_name, entries):
    counts = (entry.get(field_name) for entry in entries if entry.get(field_name))
    counter = Counter(counts)
    return counter


def get_2xx_to_all_counts(entries):
    status_code_counts = get_counts('status_code', entries)
    status_2xx_count = sum(count for status_code, count in status_code_counts.items() if 200 <= status_code <= 299)
    status_counts = sum(count for count in status_code_counts.values())
    return status_2xx_count, status_counts


def get_ip_addresses(entries):
    return {
        entry.get(field_name)
        for entry in entries
        for field_name in ('id_orig_h', 'id_reps_h', 'host')
        if entry.get(field_name) is not None
    }

# mam slownik uid -> entry_dict
def print_dict_entry_dates(log_dict):
    for uid, entries in log_dict.items():
        print(f'----- Stats for UID: {uid} -----')
        print(f'Adresy IP / hosty: {', '.join(get_ip_addresses(entries))}')
        print(f'Number of requests: {len(entries)}')
        print(f'First request: {(min(entry['ts'] for entry in entries)).strftime('%d-%m-%Y %H:%M:%S')}')
        print(f'Last request: {(max(entry['ts'] for entry in entries)).strftime('%d-%m-%Y %H:%M:%S')}')

        method_counter = get_counts('method', entries)
        method_count_sum = sum(method_counter.values())
        if method_count_sum != 0:
            for method_name, count in method_counter.items():
                print(f'- {method_name} -> {count / method_count_sum * 100.0 :.2f}%')
        else:
            print('No http methods') 

        status_2xx_count, status_counts = get_2xx_to_all_counts(entries)
        print(f'Ratio of 2xx request: {status_2xx_count / status_counts * 100.0 if status_counts != 0 else 0.0 :.2f}%')



from lab3.read_log import read_log
from lab3.log_to_dict import log_to_dict

if __name__ == '__main__':
    logs = read_log()
    log_dict = log_to_dict(logs)
    print_dict_entry_dates(log_dict)