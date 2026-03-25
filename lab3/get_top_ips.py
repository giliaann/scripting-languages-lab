from collections import Counter

from lab3.log_definition import get_index
from lab3.read_log import read_log


def get_top_ips(logs, n=10):
    ip_indexes = [get_index('id_orig_h'), get_index('id_resp_h')]
    # take ip address from each log
    ips = (log[idx] for log in logs for idx in ip_indexes if log[idx] is not None)
    counted_ips = Counter(ips)
    return counted_ips.most_common(n)

if __name__ == '__main__':
    logs = read_log()
    print(get_top_ips(logs))
