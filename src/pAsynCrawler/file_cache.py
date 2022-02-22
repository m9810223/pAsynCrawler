from functools import wraps
from pathlib import Path
from typing import Union, Callable
from inspect import iscoroutinefunction


class FileCache:
    def __init__(self, filename_transformer: Callable = lambda x: x):
        self.filename_transformer = filename_transformer
        self.method_cache_dir: Path = None

    def __call__(self, func):
        """ A decorator of file cache for async function
            use 2 additional args (url, num)
        """
        @wraps(func)
        async def a_wrapper(*args, **kwargs):
            method_self = args[0]
            method_url = args[1]
            # TODO: logging details
            # format_str = f'[{{kind:<5}}] {method_self.name}-{1+kwargs.get("num",0):0>3} -> {method_url}'
            result = None
            self.method_cache_dir = method_self.cache_dir
            if self.method_cache_dir is not None:
                result = self.read(method_url)
            if result:
                # print(format_str.format(kind='CACHE'))
                return result
            result = await func(*args, **kwargs)
            if result is None:
                return
            if self.method_cache_dir is not None:
                self.save(method_url, result)
            return result

        # # TODO: merge wrappers
        # @wraps(func)
        # def wrapper(*args, **kwargs):
        #     method_self = args[0]
        #     method_url = args[1]
        #     format_str = f'[{{kind:<5}}] {method_self.name}-{1+kwargs.get("num",0):0>3} -> {method_url}'
        #     result = None
        #     self.method_cache_dir = method_self.cache_dir
        #     if self.method_cache_dir is not None:
        #         result = self.read(method_url)
        #     if result:
        #         print(format_str.format(kind='CACHE'))
        #         return result
        #     result = func(*args, **kwargs)
        #     if self.method_cache_dir is not None:
        #         self.save(method_url, result)
        #     return result

        # if not iscoroutinefunction(func):
        #     return wrapper

        return a_wrapper

    def read(self, filename: Union[Path, str]):
        path = self.method_cache_dir/self.filename_transformer(filename)
        if path.is_file():
            return open(path).read()

    def save(self, filename: Union[Path, str], text):
        path = self.method_cache_dir/self.filename_transformer(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            f.write(text)

    def cleanup(self, url):
        # TODO
        ...


if __name__ == '__main__':
    BASE_DIR = Path(__file__).resolve().parent
    url = 'http://e.c/pa[]><th01/?p=&a=#1;e'

    class A:
        def __init__(self, cache_dir=None):
            self.cache_dir = cache_dir
            self.name = None

        @FileCache()
        def get_data(self, url):
            result = None
            print(f'get data from {url}')
            try:
                # raise Exception
                result = f'data from {url}'
            except:
                print(f'get data from {url} fail')
                return None
            print('done')
            return result

    a = A(cache_dir=BASE_DIR/'z-cache')
    # data = a.get_data(url)
    # print(data)
