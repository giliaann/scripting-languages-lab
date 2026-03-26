from lab3.log_definition import LOG_SCHEMA
from lab3.read_log import read_log


def entry_to_dict(entry):
    return {
        log_field.name : value for log_field, value in zip(LOG_SCHEMA, entry)
    }

if __name__ == '__main__':
    logs = read_log()
    print(entry_to_dict(logs[0]))
    

