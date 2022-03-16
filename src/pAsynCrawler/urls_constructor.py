from itertools import product as cartesian_product
from typing import Dict, Tuple


def _query_dict_to_qs(dic: Dict[str, str]) -> str:
    """
    {'k1': 'v1', 'k2': 'v2'} -> ?k1=v1&k2=v2
    """
    if not dic:
        return ''
    return '?' + '&'.join(f'{k}={v}' for k, v in dic.items())


def _dict__cartesian_product(dic: Dict) -> Tuple[Dict]:
    """
    {'p': ('a', 'b')} -> ({'p': 'a'}, {'p': 'b'})
    """
    return tuple(
        dict(zip(dic.keys(), vals))
        for vals in cartesian_product(*dic.values())
    )


def urls_constructor(url, *, q: Dict = None, **kwargs) -> None:
    path_dicts = _dict__cartesian_product(kwargs or {})
    query_dicts = _dict__cartesian_product(q or {})
    urls = (
        url.format(**path) + _query_dict_to_qs(query)
        for path, query in cartesian_product(path_dicts, query_dicts)
    )
    urls = tuple(urls)
    return urls


def flattener(seq, func=None):
    def _flattener(seq, func):
        for s in seq:
            if func(s):
                yield s
            else:
                yield from _flattener(s, func)
    if func is None:
        def func(x): return isinstance(x, str) or not hasattr(x, '__iter__')
    return tuple(_flattener(seq, func))


if __name__ == '__main__':
    from pprint import pprint
    url = 'https://xxx.com'
    pathes = (
        ('pa/1', 'pa/2'),
        ('pb/1',),
    )
    merged_pathes = flattener(pathes)
    pprint(merged_pathes)

    pprint(
        urls_constructor(
            f'{url}/{{path}}',
            path=merged_pathes,
            q={'k1': [1], 'k2': [2, 3]}
        )
    )
