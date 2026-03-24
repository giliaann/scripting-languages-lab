from datetime import datetime
from dataclasses import dataclass
from collections.abc import Callable
from typing import Any


def safe_parse(parser: Callable[[str], Any]) -> Callable[[str], Any]:
    return lambda x: parser(x) if x != '-' and x is not None else None


@dataclass
class LogField:
    name: str
    index: int
    parser: Callable[[str], Any] = safe_parse(str)


LOG_SCHEMA = [
    LogField("ts", 0, safe_parse(lambda x: datetime.fromtimestamp(float(x)))),
    LogField("uid", 1),
    LogField("id_orig_h", 2),
    LogField("id_orig_p", 3, safe_parse(int)),
    LogField("id_resp_h", 4),
    LogField("id_resp_p", 5, safe_parse(int)),
    LogField("trans_depth", 6, safe_parse(int)),
    LogField("method", 7),
    LogField("host", 8),
    LogField("uri", 9),
    LogField("referrer", 10),
    LogField("user_agent", 11),
    LogField("request_body_len", 12, safe_parse(int)),
    LogField("response_body_len", 13, safe_parse(int)),
    LogField("status_code", 14, safe_parse(int)),
    LogField("status_msg", 15),
    LogField("info_code", 16, safe_parse(float)),
    LogField("info_msg", 17),
    LogField("filename", 18, safe_parse(float)),
    LogField("tags", 19),
    LogField("username", 20),
    LogField("password", 21, safe_parse(float)),
    LogField("proxied", 22),
    LogField("orig_fuids", 23),
    LogField("orig_mime_types", 24),
    LogField("resp_fuids", 25),
    LogField("resp_mime_types", 26),
]

