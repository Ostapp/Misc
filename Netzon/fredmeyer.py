import hashlib
import json

import requests
from bs4 import BeautifulSoup


class FredmeyerLiveSearchStrategy:

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

        result = {'website': 'fredmeyer.com', 'hits': [], 'count': 0}

        headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}

        try:

            url = "https://www.fredmeyer.com/webapp/wcs/stores/servlet/SearchDisplay?k="+search_string+"&s=Catalog&storeId=11204&catalogId=10551&langId=-1&pageSize=12&beginIndex=0&searchSource=Q&sType=SimpleSearch&resultCatEntryType=2&showResultsPage=true&orderBy=5&pageView=image&searchTerm="+search_string

            res = requests.get(url, proxies=self.PROXY, headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            prodlist = soup(class_="itemDisplayDivs")

            if prodlist:
                for item in prodlist:
                    try:
                        prodid = item(class_="gridItemImgContainerDivs")[0].input['value']

                        result['hits'].append({
                            'product_title': item(class_="FMGridView")[0].a['title'],
                            'product_url': prodid,
                            'image_url': "https://www.fredmeyer.com" + item(class_="gridItemImgContainerDivs")[0].img['src'],
                            'item_id': 'fredmeyer-' + hashlib.md5(prodid.encode()).hexdigest()[:10]
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

        result = {'website': 'fredmeyer.com', 'hits': [], 'count': 0, 'message': ''}

        try:

            url = "https://www.fredmeyer.com/webapp/wcs/stores/servlet/ProductDisplay?urlRequestType=Base&productId=5084967&catalogId=10551&categoryId=&errorViewName=ProductDisplayErrorView&urlLangId=-1&langId=-1&top_category=&evar3=Call%2520of%2520Duty%3A%2520Infinite%2520Warfare%2520%28Xbox%2520One%2520-%2520Legacy%2520Edition%29_2&parent_category_rn=&storeId=11204"

            headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')

                hit = {'product_title': soup.find_all(attrs={"name":"description"})[0]['content'], 'product_url': url,'image_url': "https://www.fredmeyer.com" + soup(id="scrollexample")[0]['href'], 'item_id': 'fredmeyer-' + hashlib.md5(url.encode()).hexdigest()[:10]}
                result['hits'].append(hit)
                result['count'] = len(result['hits'])
                result['message'] = 'Success'

        except Exception as e:
            result['message'] = 'An exception occurred.' + str(e)

        return result
        
if __name__ == "__main__":
    strategy = FredmeyerLiveSearchStrategy()
    print('\nSEARCH TEST')
    print('SEARCH RESULT:',strategy.search('xbox'))
    print('\nPARSE TEST')
    print('PARSE RESULT:',strategy.parse("https://www.fredmeyer.com/webapp/wcs/stores/servlet/ProductDisplay?urlRequestType=Base&productId=5084967&catalogId=10551&categoryId=&errorViewName=ProductDisplayErrorView&urlLangId=-1&langId=-1&top_category=&evar3=Call%2520of%2520Duty%3A%2520Infinite%2520Warfare%2520%28Xbox%2520One%2520-%2520Legacy%2520Edition%29_2&parent_category_rn=&storeId=11204"))
