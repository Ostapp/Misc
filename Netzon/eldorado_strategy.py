    import hashlib
    import json

    import requests
    from bs4 import BeautifulSoup


    class EldoradoLiveSearchStrategy:

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

            result = {'website': 'eldorado.ru', 'hits': [], 'count': 0}

            headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}

            try:

                url = "http://www.eldorado.ru/search/catalog.php?q=" + search_string
                res = requests.get(url, proxies=self.PROXY, headers=headers)
                soup = BeautifulSoup(res.text, 'html.parser')
                prodlist = soup(class_="item")

                if prodlist:
                    for item in prodlist:
                        try:
                            prodid = "http://www.dns-shop.ru" + item(class_="ec-price-item-link")[0]['href']

                            result['hits'].append({
                                'product_title': item(class_='item-name')[0].a.text,
                                'product_url': prodid,
                                'image_url': item(class_='image')[0].a.img['data-image-desktop'],
                                'item_id': 'citilink-' + hashlib.md5(prodid.encode()).hexdigest()[:10]
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

            result = {'website': 'eldorado.ru', 'hits': [], 'count': 0, 'message': ''}

            try:

                headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
                res = requests.get(url, headers=headers)
                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, 'html.parser')

                    hit = {'product_title': soup(class_='page-title')[0].text, 'product_url': url,'image_url': soup(class_='img')[0].img['src'], 'item_id': 'dns_shop-' + hashlib.md5(url.encode()).hexdigest()[:10]}
                    result['hits'].append(hit)
                    result['count'] = len(result['hits'])
                    result['message'] = 'Success'

            except Exception as e:
                result['message'] = 'An exception occurred.' + str(e)

            return result
            
    if __name__ == "__main__":
        strategy = EldoradoLiveSearchStrategy()
        print('\nSEARCH TEST')
        print('SEARCH RESULT:',strategy.search('xbox'))
        print('\nPARSE TEST')
        print('PARSE RESULT:',strategy.parse("http://www.dns-shop.ru/product/31f82bd1b1e53330/25--vnesnij-ssd-seagate-game-drive-for-xbox-stft512400/"))
