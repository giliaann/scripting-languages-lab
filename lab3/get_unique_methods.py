from lab3.log_definition import get_index
from lab3.read_log import read_log

def get_unique_methods(logs):
    method_index = get_index('method')
    methods_set = {log[method_index] for log in logs if log[method_index] is not None}
    return list(methods_set)

if __name__ == '__main__':
    logs = read_log()
    print(sorted(get_unique_methods(logs)))