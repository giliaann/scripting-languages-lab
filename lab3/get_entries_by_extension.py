import re
from lab3.log_definition import get_index
from lab3.read_log import read_log

def get_entries_by_extension(logs, ext):
    # adding escape chars in order to make extension safe for regular expr
    safe_ext = re.escape(ext)

    pattern = re.compile(rf'\.{safe_ext}(?:[?#\s\"]|$)')

    uri_index = get_index('uri')

    return [log for log in logs if log[uri_index] and pattern.search(log[uri_index])]

if __name__ == '__main__':
    uri_index = get_index('uri')
    logs = read_log()
    filtered_logs = get_entries_by_extension(logs, 'jpg')
    for log in filtered_logs[:10]:
        print(log[uri_index])