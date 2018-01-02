    import hashlib
    import json
    import ast

    import requests
    from bs4 import BeautifulSoup


    class AmazonDeLiveSearchStrategy:

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

            result = {'website': 'amazon.de', 'hits': [], 'count': 0}

            headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}

            try:

                url = "https://www.amazon.de/s/ref=nb_sb_noss_2/259-9286682-5238636?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&url=search-alias%3Daps&field-keywords=" + search_string
                res = requests.get(url, proxies=self.PROXY, headers=headers)
                soup = BeautifulSoup(res.text, 'html.parser')
                prodlist = soup(class_="s-result-item celwidget ")

                if prodlist:
                    for item in prodlist:
                        try:
                            prodid = item('a', class_="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal")[0]['href']

                            if 'redirect' in prodid:
                                prodid = 'https://www.amazon.de' + prodid
                            result['hits'].append({
                                'product_title' : item('a', class_="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal")[0]['title']
,
                            
                                'product_url': prodid,
                                'image_url': item.img['src'],
                                'item_id': 'amazon_de-' + hashlib.md5(prodid.encode()).hexdigest()[:10]
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

            result = {'website': 'amazon.de', 'hits': [], 'count': 0, 'message': ''}

            try:

                headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
                res = requests.get(url, headers=headers)
                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, 'html.parser')

                    hit = {'product_title': soup(id='productTitle')[0].text.strip(), 'product_url': url,'image_url': soup(class_="a-dynamic-image a-stretch-vertical")[0]['data-old-hires'], 'item_id': 'amazon_de-' + hashlib.md5(url.encode()).hexdigest()[:10]}
                    result['hits'].append(hit)
                    result['count'] = len(result['hits'])
                    result['message'] = 'Success'


            except Exception as e:
                result['message'] = 'An exception occurred.' + str(e)

            return result
            
    if __name__ == "__main__":
        strategy = AmazonDeLiveSearchStrategy()
        print('\nSEARCH TEST')
        print('SEARCH RESULT:',strategy.search('xbox'))
        print('\nPARSE TEST')
        print('PARSE RESULT:',strategy.parse("https://www.amazon.de/XBOX-360-Wireless-Adapter-Controller/dp/B00JTM5OKG/ref=sr_1_13/257-8473551-2260446?s=videogames&ie=UTF8&qid=1496881159&sr=1-13-spons&keywords=xbox&psc=1"))
