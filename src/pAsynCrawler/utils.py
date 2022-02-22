from typing import Coroutine

from aiohttp import ClientSession
from aiohttp.typedefs import StrOrURL


def chunks(seq, size):
    return tuple(seq[i:i+size] for i in range(0, len(seq), size))


async def fetcher(url: StrOrURL, method: str = 'get', **kwargs) -> Coroutine:
    async with ClientSession() as session:
        return await (await session.request(method, url, **kwargs)).text()
