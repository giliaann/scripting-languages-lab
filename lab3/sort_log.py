from lab3.log_definition import LOG_SCHEMA
from lab3.read_log import read_log

def sort_log(logs, index):
    
    if index >= len(LOG_SCHEMA):
        raise IndexError(f'Tuple index out of bounds for index: {index}. Max index is: {len(LOG_SCHEMA) - 1}')
    
    #sorting function will first notice true/false differnece, and won't compare None to typed value
    return sorted(logs, key = lambda x: (x[1] is None, x[1]))

if __name__ == '__main__':
    logs = read_log()
    index = 1
    logs = sort_log(logs, index)
    for log in logs[:10]:
        print(log[index])