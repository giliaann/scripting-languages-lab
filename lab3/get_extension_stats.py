from lab3.log_definition import get_index
from collections import Counter


def extract_extension(entry):
    uri_index = get_index('uri')
    uri = entry[uri_index]

    if uri is None:
        return None
    
    clean_path = uri.split('?')[0]
    filename = clean_path.split('/')[-1]

    if '.' in filename:
        ext = filename.split('.')[-1].lower()
        return ext
    return None


def get_extension_stats(log):
    extensions = (
        ext for entry in log
        if (ext := extract_extension(entry)) is not None
    )
    return Counter(extensions) # czy warto zamieniac na slownik?


from lab3.read_log import read_log
import pprint

if __name__ == '__main__':
    logs = read_log()
    pprint.pprint(get_extension_stats(logs).most_common(50))