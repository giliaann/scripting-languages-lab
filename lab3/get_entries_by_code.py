from lab3.log_definition import get_index
from lab3.read_log import read_log

def get_entries_by_code(logs, code):
    
    try:
        code = int(code)
    except (ValueError, TypeError) as e:
        raise ValueError("Invalid code - must be an integer") from e
    
    if not (code > 99 and code < 600):
        raise ValueError("Invalid HTTP code, must be in [100,599] interval")
    
    code_index = get_index('status_code')

    return [log for log in logs if log[code_index] == code]

if __name__ == '__main__':
    logs = read_log()
    filtered_entires = get_entries_by_code(logs, 404)
    code_index = get_index('status_code')
    for log in filtered_entires[:10]:
        print(log[code_index])