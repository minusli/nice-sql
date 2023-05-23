import re
from typing import List, Any, Tuple


def parse_nsql(nsql: str, placeholder="%s") -> Tuple[str, List[Any]]:
    regex = r"{([^{}]+)}"
    params = []
    for g in re.findall(regex, nsql):
        params.append(re.sub(r"\s+", "", g))
    sql = re.sub(regex, placeholder, nsql)
    return sql, params
