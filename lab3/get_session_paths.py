from lab3.log_to_dict import log_to_dict


def get_session_paths(log):
    sessions = log_to_dict(log)
    return {
        uid : [
            entry['uri']
            for entry in sorted(
                entries, key = lambda entry: entry['ts']
                )
            ] 
            for uid, entries in sessions.items()
    }


from lab3.read_log import read_log
import pprint

if __name__ == '__main__':
    logs = read_log()
    pprint.pprint(get_session_paths(logs))