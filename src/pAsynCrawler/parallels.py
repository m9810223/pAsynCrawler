from multiprocessing import cpu_count
from multiprocessing.pool import Pool
from asyncio import gather
from typing import Coroutine, Tuple, List, Any
from traceback import format_exc
from functools import partial


class WorkError(Exception):
    pass


def _worker_wrap(worker, *args, **kwargs):
    try:
        return worker(*args, **kwargs)
    except Exception:
        print(format_exc())
        return WorkError(format_exc())


def _starmap(worker, args_list):
    return (worker(*args) for args in args_list)


async def async_worker(worker, args_list: Tuple[Tuple[Any]]) -> Coroutine:
    """ execute coroutine "worker" with args concurrently
    """
    return await gather(
        *_starmap(partial(_worker_wrap, worker), args_list)
    )


def mp_worker(worker, args_list, max_workers=2) -> List[Any]:
    processes = max(1, min(
        int(max_workers),
        len(args_list),
        cpu_count(),
    ))
    pool = Pool(processes)
    results = pool.starmap(partial(_worker_wrap, worker), args_list)
    pool.close()
    pool.join()
    return results


def add_args(first: Tuple[Any], *args) -> Tuple[Tuple[Any]]:
    """
    (1, 2), 3, 4 -> [[1, 3, 4], [2, 3, 4]]
    """
    return tuple((f, *args) for f in first)


if __name__ == '__main__':
    print(add_args((1, 2), 3, 4))

    t = [(1, 2), (3, 4)]
    print(list(zip(
        *t
    )))
