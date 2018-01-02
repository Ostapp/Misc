import hashlib
import json

import requests
import re
from bs4 import BeautifulSoup


class ParisLiveSearchStrategy:

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
        headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}

        splash = 'http://localhost:8050/render.html'

        result = {'website': 'paris.cl', 'hits': [], 'count': 0}

        try:
            
            query_url = "https://www.paris.cl/webapp/wcs/stores/servlet/SearchDisplay?storeId=10801&catalogId=40000000629&langId=-5&pageSize=30&beginIndex=0&searchSource=Q&sType=SimpleSearch&resultCatEntryType=2&showResultsPage=true&pageView=image&searchTerm=" + search_string
            query_res = requests.get(query_url, headers=headers)
            result_url = query_res.url
            rendered_html = requests.get(splash, params={'url':result_url}, proxies=self.PROXY, headers=headers)

            soup = BeautifulSoup(rendered_html.text, 'html.parser')
            prodlist = soup(id='product')

            if prodlist:
                for item in prodlist:
                    try:
                        prodid = item(class_='description_fixedwidth')[0].a['href']

                        result['hits'].append({
                            'product_title' : item(class_='description_fixedwidth')[0].a.text.strip(),

                            'product_url': prodid,
                            'image_url': item.img['data-src'],
                            'item_id': 'paris-' + hashlib.md5(prodid.encode()).hexdigest()[:10]
                        })

                    except Exception as e:
                        pass

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

        splash = 'http://localhost:8050/render.html'

        headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}

        rendered_html = requests.get(splash, params={'url':url}, proxies=self.PROXY, headers=headers)

        soup = BeautifulSoup(rendered_html.text, "html.parser")

        result = {'website': 'paris.cl', 'hits': [], 'count': 0, 'message': ''}

        try:
            s = soup(class_='s7thumb')[0]['style']
            link_start_from_end = s[::-1].find('(')
            link_start_from_beginning = s[::-1].find(')')+1
            s_reversed = s[::-1]
            s_link_reversed = s_reversed[link_start_from_beginning:link_start_from_end]
            s_link = s_link_reversed[::-1]

            small_size = re.search('wid=\d*&hei=\d*', s_link)
            large_size = re.sub(r'\d+','500',small_size.group(0))
            final_link = s_link.replace(small_size.group(0),large_size)


            headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')

                hit = {'product_title': soup('h1',class_='detalles-titulo')[0].text, 'product_url': url,'image_url': final_link, 'item_id': 'paris-' + hashlib.md5(url.encode()).hexdigest()[:10]}
                result['hits'].append(hit)
                result['count'] = len(result['hits'])
                result['message'] = 'Success'


        except Exception as e:
            result['message'] = 'An exception occurred.' + str(e)

        return result
        
if __name__ == "__main__":
    strategy = ParisLiveSearchStrategy()
    print('\nSEARCH TEST')
    print('SEARCH RESULT:',strategy.search('xbox'))
    print('\nPARSE TEST')
    print('PARSE RESULT:',strategy.parse("https://www.paris.cl/tienda/es/paris/tecnologia/xbox-one/consola-xbox-one-s-500gb--control--forza-horizon-3--3-meses-xbox-live-208068-ppp-"))
