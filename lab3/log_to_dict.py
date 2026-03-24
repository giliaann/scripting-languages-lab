from collections import defaultdict
from lab3.log_definition import LOG_SCHEMA, get_index
from lab3.entry_to_dict import entry_to_dict


def log_to_dict(logs):
    uid_index = get_index('uid')

    if not uid_index:
        raise ValueError('Uid index does not exist in entries')

    sessions = defaultdict(list)

    for log in logs:
        uid = log[uid_index]
        entry_dict = entry_to_dict(log)
        sessions[uid].append(entry_dict)
    
    return sessions


