from collections import Counter




def analyze_log(log):
    if not log:
        return None # Brak danych
    
    ips = Counter()
    uris = Counter()
    methods = Counter()
    user_agents = Counter()

    error_count = 0
    successful_requests = 0

    for entry in log:
        # jedyne miejsce gdzie rozpakowujemy krotke
        _, _, ip, _, _, _, _, method, _, uri, _, user_agent, _, _, status_code, *_ = entry

        if ip is not None:
            ips[ip] += 1

        if uri is not None:
            uris[uri] += 1

        if method is not None:
            methods[method] += 1

        if user_agent is not None:
            user_agents[user_agent] += 1

        if status_code is not None:
            if status_code >= 400:
                error_count += 1
            else:
                successful_requests += 1

    total_requests = len(log)
    error_rate = error_count / total_requests * 100 if total_requests > 0 else 0.0

    return {
        'most_frequent_ip' : ips.most_common(1) if ips else None,
        'most_frequent_uri' : uris.most_common(1) if uris else None,
        'method_distribution' : dict(methods),
        'error_count' : error_count,
        # dodatkowe
        'unique_ips_count' : len(ips),
        'error_perc_rate' : error_rate,
        'most popular user_agent' : user_agents.most_common(1) if user_agents else None
    }




from lab3.read_log import read_log
import pprint

if __name__ == '__main__':
    logs = read_log()
    pprint.pprint(analyze_log(logs))