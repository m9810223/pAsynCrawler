from pathlib import Path
from pprint import pprint

from functools import partial
from json import loads

from bs4 import BeautifulSoup
from pAsynCrawler import AsynCrawler, flattener


BeautifulSoup = partial(BeautifulSoup, features="html.parser")


url_root = 'https://www.rakuten.com.tw'


def parser_0(response_text):
    soup = BeautifulSoup(response_text)
    menus = soup.select('.top-mainmenu > ul > li > span > .menu-title > a')
    menus = menus[1:]
    menus = menus[:1]  # DEV
    datas = tuple(x.text for x in menus)
    urls = tuple(url_root + x.attrs['href'] for x in menus)
    return datas, urls


def parser_1(response_text):
    soup = BeautifulSoup(response_text)
    # lv 2
    menus_2 = soup.select('.cl-top-block .category-content > li > .ui-hover > a')
    menus_2 = menus_2[1:]  # DEV
    datas_2 = tuple(x.text for x in menus_2)
    urls_2 = tuple(x.attrs['href'] for x in menus_2)
    # lv 3
    menus_3 = soup.select('.cl-top-block .category-content > li > .nav_popup > ul > li > a')
    menus_3 = menus_3[1:]  # DEV
    datas_3 = tuple(x.text for x in menus_3)
    urls_3 = tuple(x.attrs['href'] for x in menus_3)
    # lv 4
    menus_4 = soup.select(
        '.cl-top-block .category-content > li > .nav_popup > ul > li > ul.keyword-list > li > a'
    )
    menus_4 = menus_4[1:]  # DEV
    datas_4 = tuple(x.text for x in menus_4)
    urls_4 = tuple(x.attrs['href'] for x in menus_4)
    return datas_2, urls_2, datas_3, urls_3, datas_4, urls_4


def parser_4(response_text):
    soup = BeautifulSoup(response_text)
    data_source = soup.select_one('.js-react-on-rails-component[data-component-name="SearchPage"]')
    products = loads(data_source.text).get('initialData', {}).get('searchPage', {}).get('result', {}).get('items', {})
    if not products:
        raise ValueError
    products = products[1:]  # DEV
    datas_5 = tuple(x.get('itemName', '') for x in products)
    urls_5 = tuple(x.get('itemUrl', '') for x in products)
    return datas_5, urls_5


if __name__ == '__main__':
    BASE_DIR = Path(__file__).resolve().parent
    ac = AsynCrawler(cache_dir=BASE_DIR/'.cache', asy_fetch=2, mp_parse=6)
    datas_1, urls_1 = ac.fetch_and_parse(parser_0, [url_root])
    # pprint(datas_1)

    datas_2, urls_2, datas_3, urls_3, datas_4, urls_4 = ac.fetch_and_parse(parser_1, flattener(urls_1))
    # print(datas_2)
    # pprint(urls_2)
    # print(datas_3)
    # pprint(urls_3)
    # print(datas_4)
    # pprint(urls_4)

    urls_4 = flattener(urls_4)
    urls_4 = urls_4[:10]  # DEV

    # parse_page_nums = 30 # TODO: parse ssome pages, qs: '?p=X'
    datas_5, urls_5 = ac.fetch_and_parse(parser_4, urls_4)
    pprint(datas_5)
    # pprint(urls_5)
