from collections import Counter


def count_status_classes(logs):
    status_index = 14
    
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
