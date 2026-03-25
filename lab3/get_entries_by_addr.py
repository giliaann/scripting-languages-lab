import ipaddress
from lab3.log_definition import get_index
from lab3.read_log import read_log


def validate_ipv4_addr(addr):
    try:
        ipaddress.IPv4Address(addr)
        return True
    except ipaddress.AddressValueError:
        return False 

def get_entries_by_addr(logs, addr):
    
    comparison_index = get_index('id_orig_h' if validate_ipv4_addr(addr) else 'host')

    return [log for log in logs if log[comparison_index] == addr]

if __name__ == '__main__':
    logs = read_log()
    filtered_logs = get_entries_by_addr(logs, '192.168.202.110')
    ip_orig_h_index = get_index('id_orig_h')
    for log in filtered_logs[:10]:
        print(log[ip_orig_h_index])
    
