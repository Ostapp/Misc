    import hashlib
    import json
    import ast

    import requests
    from bs4 import BeautifulSoup


    class AmazonCoJpLiveSearchStrategy:

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

            result = {'website': 'amazon.co.jp', 'hits': [], 'count': 0}

            headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}

            try:

                url = "https://www.amazon.co.jp/s/ref=nb_sb_noss_2/356-5375297-9893143?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&url=search-alias%3Daps&field-keywords=" + search_string
                res = requests.get(url, proxies=self.PROXY, headers=headers)
                soup = BeautifulSoup(res.text, 'html.parser')
                prodlist = soup(class_="s-result-item celwidget ")

                if prodlist:
                    for item in prodlist:
                        try:
                            prodid = item('a', class_="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal")[0]['href']

                            if 'redirect' in prodid:
                                prodid = 'https://www.amazon.co.jp' + prodid
                            result['hits'].append({
                                'product_title' : item('a', class_="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal")[0]['title']
,
                            
                                'product_url': prodid,
                                'image_url': item.img['src'],
                                'item_id': 'amazon_co_jp-' + hashlib.md5(prodid.encode()).hexdigest()[:10]
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

            result = {'website': 'amazon.co.jp', 'hits': [], 'count': 0, 'message': ''}

            try:

                headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
                res = requests.get(url, headers=headers)
                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, 'html.parser')

                    hit = {'product_title': soup(id='productTitle')[0].text.strip(), 'product_url': url,'image_url': soup(class_="imgTagWrapper")[0].img['data-old-hires'], 'item_id': 'amazon_de-' + hashlib.md5(url.encode()).hexdigest()[:10]}
                    result['hits'].append(hit)
                    result['count'] = len(result['hits'])
                    result['message'] = 'Success'


            except Exception as e:
                result['message'] = 'An exception occurred.' + str(e)

            return result
            
    if __name__ == "__main__":
        strategy = AmazonCoJpLiveSearchStrategy()
        print('\nSEARCH TEST')
        print('SEARCH RESULT:',strategy.search('xbox'))
        print('\nPARSE TEST')
        print('PARSE RESULT:',strategy.parse("https://www.amazon.co.jp/%E6%9C%9F%E9%96%93%E9%99%90%E5%AE%9A%E4%BE%A1%E6%A0%BC-Xbox-500GB-Kinect-7UV-00262/dp/B01KWYZZUI/ref=sr_1_19/357-3871080-8579814?ie=UTF8&qid=1496886205&sr=8-19&keywords=xbox"))
