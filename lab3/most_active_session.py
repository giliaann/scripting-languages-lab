


def most_active_session(log_dict):
    return max(log_dict.items(), key = lambda item: len(item[1]))


from lab3.read_log import read_log
from lab3.log_to_dict import log_to_dict

if __name__ == '__main__':
    logs = read_log()
    log_dict = log_to_dict(logs)
    item = most_active_session(log_dict)
    print(f'{item[0]} -> {len(item[1])}')