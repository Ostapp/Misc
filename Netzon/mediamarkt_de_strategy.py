import hashlib
import json

import requests
from bs4 import BeautifulSoup


class MediamarktDeLiveSearchStrategy:

    def __init__(self, proxy = None):

        """
        Initialize class

        :param proxy: proxy for request
        """

        self.PROXY = proxy

    def search(self, search_string):

        """
        Search for keyword in website and return top 100 hits

        :param search_string: Keyword to search
        :return: top 100 hits dict
        """

        result = {'website': 'mediamarkt.de', 'hits': [], 'count': 0}

        headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}

        try:

            splash = 'http://localhost:8050/render.html'
            query_url = "http://www.mediamarkt.de/de/search.html?storeId=48535&langId=-3&searchProfile=onlineshop&channel=mmdede&searchParams=&query=" + search_string
            query_res = requests.get(query_url, proxies=self.PROXY, headers=headers)
            result_url = query_res.url

            rendered_html = requests.get(splash, params={'url':result_url}, proxies=self.PROXY, headers=headers)

            soup = BeautifulSoup(rendered_html.text, "html.parser")

            prodlist = soup(class_="product-wrapper")

            if prodlist:
                for item in prodlist:
                    try:
                        prodid = "https://www.mediamarkt.de" + item.h2.a['href']

                        result['hits'].append({
                            'product_title' : item.h2.text.strip(),
                        
                            'product_url': prodid,
                            'image_url': 'http:' + item(class_='photo-wrapper')[0].a.img['src'],
                            'item_id': 'mediamarkt_de-' + hashlib.md5(prodid.encode()).hexdigest()[:10]
                        })

                    except Exception as e:
                        print e

            result['count'] = len(result['hits'])
            result['message'] = 'Success'

        except Exception as e:
            result['message'] = 'An exception occurred.' + str(e)

        return result

    def parse(self, url):

        """
        Parse data from url

        :param url: url to parse
        :return: parsed data dict
        """

        

        result = {'website': 'mediamarkt.de', 'hits': [], 'count': 0, 'message': ''}

        try:

            headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')

                hit = {'product_title': soup('div', class_='details')[0].h1.text, 'product_url': url,'image_url': 'http:' + soup('a', class_='zoom')[0].img['src'], 'item_id': 'mediamarkt_de-' + hashlib.md5(url.encode()).hexdigest()[:10]}
                result['hits'].append(hit)
                result['count'] = len(result['hits'])
                result['message'] = 'Success'


        except Exception as e:
            result['message'] = 'An exception occurred.' + str(e)

        return result
        
if __name__ == "__main__":
    os.system('sudo docker run scrapinghub/splash')
    strategy = MediamarktDeLiveSearchStrategy()
    print('\nSEARCH TEST')
    print('SEARCH RESULT:',strategy.search('playstation'))
    print('\nPARSE TEST')
    print('PARSE RESULT:',strategy.parse("http://www.mediamarkt.de/de/product/_playstation-4-slim-500gb-2-dualshock4-controller-ps4-konsolen-2221363.html"))

