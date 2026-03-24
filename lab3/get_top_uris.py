from collections import Counter


def get_top_uris(logs, n=10):
    uri_index = 9
    uris = (log[uri_index] for log in logs if log[uri_index] is not None)
    counted_uris = Counter(uris)
    return counted_uris.most_common(n)
