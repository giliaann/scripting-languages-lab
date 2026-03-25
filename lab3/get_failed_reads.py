from lab3.log_definition import get_index
from lab3.read_log import read_log

def get_failed_reads(logs, merge = False):
    
    code_index = get_index('status_code')
    
    list_4xx = []
    list_5xx = []

    for log in logs:
        
        if log[code_index] is None:
            continue

        log_code_digit = log[code_index]//100

        if log_code_digit == 4:
            list_4xx.append(log)

        elif log_code_digit == 5:
            list_5xx.append(log)


    if merge:
        list_4xx.extend(list_5xx)
        return list_4xx
    else:
        return (list_4xx, list_5xx)

if __name__ == '__main__':
    code_index = get_index('status_code')
    logs = read_log()

    filtered_logs = get_failed_reads(logs, True)
    for log in filtered_logs[:10]:
        print(log[code_index])

    (filtered_logs_4xx, filtered_logs_5xx) = get_failed_reads(logs, False)
    for log_4xx, log_5xx in zip(filtered_logs_4xx[:10], filtered_logs_5xx[:10]):
        print(f"{log_4xx[code_index]} - {log_5xx[code_index]}")