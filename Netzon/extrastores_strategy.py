    import hashlib
    import json
    import ast

    import requests
    from bs4 import BeautifulSoup


    class ExtrastoresLiveSearchStrategy:

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

            result = {'website': 'extrastores.com', 'hits': [], 'count': 0}

            headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}

            try:

                url = "http://www.extrastores.com/en-sa/search?page=1&q=" + search_string
                res = requests.get(url, proxies=self.PROXY, headers=headers)
                soup = BeautifulSoup(res.text, 'html.parser')
                prodlist = soup(class_='productbox')

                if prodlist:
                    for item in prodlist:
                        try:
                            href_string = item.a['href']
                            q1_index = href_string.find('"') + 1
                            q2_index = q1_index + href_string[q_index+1:].find('"')
                            href = href_string[q1_index:q2_index]

                            prodid = "http://www.extrastores.com" + href

                            result['hits'].append({
                                'product_title' : item(class_="titlemaxheight")[0].text.strip(),
                            
                                'product_url': prodid,
                                'image_url': item(class_='prodimg')[0].img['src'],
                                'item_id': 'extrastores-' + hashlib.md5(prodid.encode()).hexdigest()[:10]
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

            result = {'website': 'extrastores.com', 'hits': [], 'count': 0, 'message': ''}

            try:

                headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
                res = requests.get(url, headers=headers)
                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, 'html.parser')

                    soup(class_='proddscrpt')[0].h1.span.extract()

                    hit = {'product_title': soup(class_='proddscrpt')[0].h1.text.strip(), 'product_url': url,'image_url': soup(class_='mainpic')[1].img['src'], 'item_id': 'extrastores-' + hashlib.md5(url.encode()).hexdigest()[:10]}
                    result['hits'].append(hit)
                    result['count'] = len(result['hits'])
                    result['message'] = 'Success'


            except Exception as e:
                result['message'] = 'An exception occurred.' + str(e)

            return result
            
    if __name__ == "__main__":
        strategy = ExtrastoresLiveSearchStrategy()
        print('\nSEARCH TEST')
        print('SEARCH RESULT:',strategy.search('xbox'))
        print('\nPARSE TEST')
        print('PARSE RESULT:',strategy.parse("http://www.extrastores.com/en-sa/games/xbox/fifa-16-xbox-one-b-183005?q=xbox&r=11"))
