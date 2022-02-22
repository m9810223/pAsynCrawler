# pAsynCrawler

<p align="left">
  <a href="https://pypi.org/project/pAsynCrawler" target="_blank">
    <img src="https://img.shields.io/pypi/v/pAsynCrawler?color=%2334D058&label=pypi%20package" alt="Package version">
  </a>
</p>

## Installation

```shell
pip install pAsynCrawler
```

## Features

- Fetch data - `Asynchronously`
- Parse data - with `multiprocessing`

## Demo

[demo code](https://github.com/m9810223/pAsynCrawler/tree/master/demos)

## Example

```python
from bs4 import BeautifulSoup
from pAsynCrawler import AsynCrawler, flattener


def parser_0(response_text):
    soup = BeautifulSoup(response_text)
    menus = soup.select('ul > li > span > a')
    datas = tuple(x.text for x in menus)
    urls = tuple(x.attrs['href'] for x in menus)
    return (datas, urls)


def parser_0(response_text):
    soup = BeautifulSoup(response_text)
    menus = soup.select('ul > li > a')
    datas = tuple(x.text for x in menus)
    urls = tuple(x.attrs['href'] for x in menus)
    return (datas, urls)


if __name__ == '__main__':
    ac = AsynCrawler(asy_fetch=20, mp_parse=8)
    datas_1, urls_1 = ac.fetch_and_parse(parser_0, ['https://www.example.com'])
    datas_2, urls_2 = ac.fetch_and_parse(parser_1, flattener(urls_1))

```
