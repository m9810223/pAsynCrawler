from pprint import pprint
from pathlib import Path
from functools import partial

from bs4 import BeautifulSoup
from pAsynCrawler import AsynCrawler


BeautifulSoup = partial(BeautifulSoup, features="html.parser")
url_root = 'https://www.kingstone.com.tw'


def parser_0(response_text):
    if not response_text:
        return
    soup = BeautifulSoup(response_text)
    menus = soup.select(
        '#header_megamenu .navLv0 > li > a'
    )
    menus.pop(4)  # ignore '/ebook'
    menus = menus[:-1]
    # menus = menus[:2]  # dev
    datas = tuple(
        x.text for x in menus
    )
    next_urls = tuple(
        url_root + x.attrs['href'] for x in menus
    )
    return datas, next_urls


def parser_1(response_text, prev_data):
    soup = BeautifulSoup(response_text)
    menus = soup.select(
        '.navcolumn_classlevel > ul > li > a'
    )
    # menus = menus[:5]  # DEV
    datas = tuple(
        f'{prev_data} > {x.text}' for x in menus
    )
    next_urls = tuple(
        url_root + x.attrs['href'] for x in menus
    )
    return datas, next_urls


def parser_2(response_text, prev_data):
    soup = BeautifulSoup(response_text)
    children = soup.select('a.on + ul > li > a')
    # children = children[:4]  # DEV
    datas = tuple(
        f'{prev_data} > {x.text}' for x in children
    )
    next_urls = tuple(
        url_root + x.attrs['href'] for x in children
    )
    return datas, next_urls


parser_3 = parser_2


def parser_4(response_text):
    soup = BeautifulSoup(response_text)
    pagetotal = soup.select_one('.pagetotal')
    pagetotal = pagetotal.text.rsplit('/', 1)[-1]
    return pagetotal, ()


# def parser_product(response_text):
#     soup = BeautifulSoup(response_text)
#     products = soup.select('.displayunit > div > .beta_display > .pdnamebox > a')
#     results = (
#         {'path': x.attrs['href'], 'name': x.text} for x in products
#     )
#     results = tuple(results)
#     return results


if __name__ == '__main__':
    BASE_DIR = Path(__file__).resolve().parent
    ac = AsynCrawler(cache_dir=BASE_DIR/'.cache')
    datas, next_urls = ac.fetch_and_parse(parser_0, [url_root])
    pprint(datas)
    pprint(next_urls)
