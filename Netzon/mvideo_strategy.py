    import hashlib
    import json
    import ast

    import requests
    from bs4 import BeautifulSoup


    class MvideoLiveSearchStrategy:

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

            result = {'website': 'mvideo.ru', 'hits': [], 'count': 0}

            headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}

            try:

                url = "http://www.mvideo.ru/product-list-page?q=" + search_string + "&region_id=1&limit=12"
                res = requests.get(url, proxies=self.PROXY, headers=headers)
                soup = BeautifulSoup(res.text, 'html.parser')
                prodlist = soup(class_="product-tile")

                if prodlist:
                    for item in prodlist:
                        try:
                            prodid = "http://www.mvideo.ru" + item(class_="product-tile-picture-link")[0]['href']

                            result['hits'].append({
                                'product_title' : ast.literal_eval(item('a', class_="product-tile-picture-link")[0].attrs['data-product-info'])['productName'],
                            
                                'product_url': prodid,
                                'image_url': "http:" + item.a.img['data-original'],
                                'item_id': 'mvideo-' + hashlib.md5(prodid.encode()).hexdigest()[:10]
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

            result = {'website': 'mvideo.ru', 'hits': [], 'count': 0, 'message': ''}

            try:

                headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
                res = requests.get(url, headers=headers)
                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, 'html.parser')

                    hit = {'product_title': soup('h1',class_="product-title sel-product-title")[0].text, 'product_url': url,'image_url': "http:" + soup('a',class_="wrapper")[0]['data-src'], 'item_id': 'mvideo_shop-' + hashlib.md5(url.encode()).hexdigest()[:10]}
                    result['hits'].append(hit)
                    result['count'] = len(result['hits'])
                    result['message'] = 'Success'

            except Exception as e:
                result['message'] = 'An exception occurred.' + str(e)

            return result
            
    if __name__ == "__main__":
        strategy = MvideoLiveSearchStrategy()
        print('\nSEARCH TEST')
        print('SEARCH RESULT:',strategy.search('xbox'))
        print('\nPARSE TEST')
        print('PARSE RESULT:',strategy.parse("http://www.mvideo.ru/products/geimpad-dlya-xbox-360-media-guitar-hero-live-gitara-40064191"))
