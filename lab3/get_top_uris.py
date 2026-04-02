from collections import Counter
from lab3.log_definition import get_index


def get_top_uris(logs, n=10):
    uri_index = get_index('uri')
    uris = (log[uri_index] for log in logs if log[uri_index] is not None)
    counted_uris = Counter(uris)
    return counted_uris.most_common(n)


from lab3.read_log import read_log
import pprint

if __name__ == '__main__':
    logs = read_log()
    pprint.pprint(get_top_uris(logs))
