import asyncio
from typing import Tuple, Callable, List
from re import sub
from itertools import chain

from .parallels import async_worker, mp_worker, add_args, WorkError
from .file_cache import FileCache
from .utils import fetcher as default_fetcher, chunks


class AsynCrawler:
    def __init__(
        self,
        cache_dir=None,
        fetcher=default_fetcher,
        asy_fetch=2,
        mp_parse=2,
    ):
        self.cache_dir = cache_dir
        self.fetcher = fetcher
        self.asy_fetch = asy_fetch
        self.mp_parse = mp_parse

    @FileCache(lambda url: sub(pattern='[\\\\/:*?"><".{}\[\]]+', repl='-', string=url,))
    async def __fetch(self, url: str, start_id: int) -> str:
        format_str = f'[{{kind:<5}}] {1+start_id:0>3} -> {url}'
        result = None
        try:
            print(format_str.format(kind='go...'))
            result = await self.fetcher(url)  # TODO: retry
        except Exception:
            print(format_str.format(kind='FAIL'))
            return None
        print(format_str.format(kind='DONE'))
        return result

    def _fetch(self, urls, start_id: int = 0) -> List[str]:
        return asyncio.run(async_worker(
            self.__fetch,
            zip(urls, range(start_id, start_id+len(urls)))
        ))

    def _batch_fetch(self, urls) -> Tuple[str]:
        urls_chunks = chunks(urls, size=self.asy_fetch)
        fetched_result = tuple(
            self._fetch(urls_chunks[i], start_id=self.asy_fetch*i)
            for i in range(len(urls_chunks))
        )
        return tuple(chain(*fetched_result))

    def fetch(self, urls: Tuple[str]) -> Tuple[str]:
        return self._batch_fetch(urls)

    def parse(self, parser, responses, *args_list):
        parse_results = mp_worker(
            parser,
            add_args(responses, *args_list),
            self.mp_parse
        )
        results = []
        for r in parse_results:
            if r is not None and not isinstance(r, WorkError):
                results.append(r)
            else:
                results.append(((),))
        return list(zip(*results))

    def fetch_and_parse(self, parser: Callable, urls: Tuple, *args_list):
        responses = self.fetch(urls)
        if args_list is None:
            args_list = ((),) * len(responses)
        return self.parse(parser, responses, *args_list)
