from collections import Counter
from lab3.log_definition import LOG_SCHEMA, get_index


def count_status_classes(logs):
    status_index = get_index('status_code')

    if not status_index:
        raise ValueError('Status index does not exist in entries')
    
    classes = (
        f'{int(log[status_index] // 100)}xx'
        for log in logs
        if log [status_index] is not None
    )

    counter = Counter(classes)
    result = {
        '2xx' : 0,
        '3xx' : 0,
        '4xx' : 0,
        '5xx' : 0,
    }
    result.update(counter)
    return result


from lab3.read_log import read_log

if __name__ == '__main__':
    logs = read_log()
    print(count_status_classes(logs))