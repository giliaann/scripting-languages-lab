from lab3.log_definition import get_index
from lab3.read_log import read_log
from collections import Counter


def count_by_method(logs):
    method_index = get_index('method')
    counted_methods = Counter((log[method_index] for log in logs if log[method_index] is not None))
    return [{f"{method}" : count} for method, count in counted_methods.items()]

if __name__ == '__main__':
    logs = read_log()
    print(count_by_method(logs))
    
