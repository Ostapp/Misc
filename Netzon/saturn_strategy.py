    import hashlib
    import json
    import ast

    import requests
    from bs4 import BeautifulSoup


    class SaturnLiveSearchStrategy:    

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

            result = {'website': 'saturn.de', 'hits': [], 'count': 0}

            headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}

            try:

                url = "http://www.saturn.de/de/search.html?query=" + search_string + "&searchProfile=onlineshop&channel=sedede"
                res = requests.get(url, proxies=self.PROXY, headers=headers)
                soup = BeautifulSoup(res.text, 'html.parser')
                prodlist = soup(class_="product-wrapper")

                if prodlist:
                    for item in prodlist:
                        try:
                            prodid = "http://www.saturn.de" + item(class_="manufacturer clickable")[0]['data-clickable-href']

                            result['hits'].append({
                                'product_title' : item.h2.text.strip()
,
                            
                                'product_url': prodid,
                                'image_url': "http:" + item(class_='photo-wrapper')[0].img['data-original'],
                                'item_id': 'saturn-' + hashlib.md5(prodid.encode()).hexdigest()[:10]
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

            result = {'website': 'saturn.de', 'hits': [], 'count': 0, 'message': ''}

            try:

                headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
                res = requests.get(url, headers=headers)
                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, 'html.parser')

                    hit = {'product_title': soup('h1',{'itemprop':'name'})[0].text, 'product_url': url,'image_url': "http:" + soup(class_="zoom")[0].img['src'], 'item_id': 'saturn-' + hashlib.md5(url.encode()).hexdigest()[:10]}
                    result['hits'].append(hit)
                    result['count'] = len(result['hits'])
                    result['message'] = 'Success'


            except Exception as e:
                result['message'] = 'An exception occurred.' + str(e)

            return result
            
    if __name__ == "__main__":
        strategy = SaturnLiveSearchStrategy()
        print('\nSEARCH TEST')
        print('SEARCH RESULT:',strategy.search('xbox'))
        print('\nPARSE TEST')
        print('PARSE RESULT:',strategy.parse("http://www.saturn.de/de/product/_microsoft-xbox-one-s-500gb-konsole-minecraft-bundle-2227206.html"))
