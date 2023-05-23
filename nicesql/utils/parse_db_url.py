from typing import Dict
from urllib.parse import urlparse, parse_qs


def parse_db_url(url: str) -> Dict[str, str | int]:
    url = url.strip()
    r = urlparse(url)
    engine_type = r.scheme
    engine_host = r.hostname
    engine_port = r.port
    engine_database = r.path.strip("/")
    engine_params = parse_qs(r.query)

    kv = {}
    for k, v in engine_params.items():
        if v:
            kv[k] = v[0]

    kv['type'] = engine_type
    kv['host'] = engine_host
    kv['port'] = engine_port
    kv['database'] = engine_database

    return kv
