import hashlib
import json

import requests
from bs4 import BeautifulSoup


class AmazonCoUkLiveSearchStrategy:

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

        result = {'website': 'AMAZON.CO.UK', 'hits': [], 'count': 0}

        headers = {'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1; rv:9.0.1) Gecko/20100101 Firefox/9.0.1'}

        try:
            url = "https://www.amazon.co.uk/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=" + \
                  search_string + "&rh=i%3Aaps%2Ck%3A" + search_string
            url = url.replace("+&+", "+%26+")
            res = requests.get(url, proxies=self.PROXY, headers=headers)

            soup = BeautifulSoup(res.text, 'html.parser')
            prodlist = soup.select("li.s-result-item.celwidget")
            
            if prodlist:
                for item in prodlist:
                    try:
                        prodid = item.select(".a-link-normal.s-access-detail-page.s-color-twister-title-link"
                                             ".a-text-normal")[0].attrs['href']
                        result['hits'].append({
                            'product_title': item.select(
                                ".a-link-normal.s-access-detail-page.s-color-twister-title-link.a-text-normal > h2")[
                                0].get_text().strip(),
                            'product_url': prodid,
                            'image_url': item.select("img")[0].attrs["src"],
                            'item_id': 'amazon_co_uk-' + hashlib.md5(prodid.encode()).hexdigest()[:10]
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

        result = {'website': 'AMAZON.CO.UK', 'hits': [], 'count': 0, 'message': ''}

        try:
            headers = {'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1; rv:9.0.1) Gecko/20100101 Firefox/9.0.1'}
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')

                hit = {'product_title': soup.select("#title")[0].get_text().strip(), 'product_url': url,
                       'image_url': soup.select("span > img")[0].attrs["src"],
                       'item_id': 'amazon_co_uk-' + hashlib.md5(url.encode()).hexdigest()[:10]}
                result['hits'].append(hit)
                result['count'] = len(result['hits'])
                result['message'] = 'Success'

        except Exception as e:
            result['message'] = 'An exception occurred.' + str(e)

        return result
        
if __name__ == "__main__":
    strategy = AmazonCoUkLiveSearchStrategy()
    print('\nSEARCH TEST')
    print('SEARCH RESULT:',strategy.search('microsoft'))
    print('\nPARSE TEST')
    print('PARSE RESULT:',strategy.parse('https://www.amazon.co.uk/Microsoft-Office-2016-Professional-Plus/dp/B01DYRABLI/ref=sr_1_2?ie=UTF8&qid=1496028875&sr=8-2&keywords=microsoft'))
