    import hashlib
    import json

    import requests
    from bs4 import BeautifulSoup


    class UaeSharafdgComLiveSearchStrategy:

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

                result = {'website': 'uae.sharafdg.com', 'hits': [], 'count': 0}

                headers = {"accept":"application/json","Accept-Encoding":"gzip, deflate, br","Accept-Language":"en-US,en;q=0.8,hu;q=0.6", "Connection":"keep-alive","Content-Length":"700","content-type":"application/x-www-form-urlencoded","Host":"9khjlg93j1-dsn.algolia.net", "Origin":"https://uae.sharafdg.com","Referer":"https://uae.sharafdg.com/?q="+ search_string +"&post_type=product&algolia=true","User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","x-algolia-application-id":"9KHJLG93J1","x-algolia-api-key":"e81d5b30a712bb28f0f1d2a52fc92dd0","x-algolia-agent":"Algolia for vanilla JavaScript 3.22.1;JS Helper 2.20.1"}

                data = {"requests":[{"indexName":"products_index","params":"query="+ search_string +"&hitsPerPage=24&maxValuesPerFacet=20&page=0&attributesToRetrieve=permalink,permalink_ar,post_title,post_title_ar,discount,discount_val,images,price,promotion_offer_json,regular_price,sale_price&attributesToHighlight=post_title,post_title_ar&getRankingInfo=1&facetFilters=[\"post_status:publish\"]&facets=[\"taxonomies.attr.Screen Size\",\"taxonomies.attr.Brand\",\"taxonomies.attr.Color\",\"taxonomies.attr.OS\",\"taxonomies.attr.Internal Memory\",\"taxonomies.attr.Battery Capacity\",\"price\",\"taxonomies.taxonomies_hierarchical.product_cat.lvl0\"]&tagFilters="}]}

                url = "https://9khjlg93j1-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%203.22.1%3BJS%20Helper%202.20.1&x-algolia-application-id=9KHJLG93J1&x-algolia-api-key=e81d5b30a712bb28f0f1d2a52fc92dd0"    

                try:

                    res = requests.post(url,headers=headers, data=json.dumps(data))
                    jres = res.json()
                    prodlist = jres['results'][0]['hits']

                    if prodlist:
                        for item in prodlist:
                            try:
                                prodid = item['permalink']
                                
                                result['hits'].append({
                                    'product_title': item['post_title'],
                                    'product_url': prodid,
                                    'image_url': item['images'],
                                    'item_id': 'sharafdg-' + hashlib.md5(prodid.encode()).hexdigest()[:10]
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

                result = {'website': 'uae.sharafdg.com', 'hits': [], 'count': 0, 'message': ''}

                try:

                    headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
                    res = requests.get(url, headers=headers)

                    if res.status_code == 200:

                        soup = BeautifulSoup(res.text)

                        hit = {'product_title': soup('h1',class_='product_title entry-title')[0].text, 'product_url': url,'image_url':soup(class_="sdg-ratio")[0].img['src'], 'item_id': 'sharafdg-' + hashlib.md5(url.encode()).hexdigest()[:10]}
                        result['hits'].append(hit)
                        result['count'] = len(result['hits'])
                        result['message'] = 'Success'

                except Exception as e:
                    result['message'] = 'An exception occurred.' + str(e)

                return result
            
    if __name__ == "__main__":
        strategy = UaeSharafdgComLiveSearchStrategy()
        print('\nSEARCH TEST')
        print('SEARCH RESULT:',strategy.search('playstation'))
        print('\nPARSE TEST')
        print('PARSE RESULT:',strategy.parse("https://uae.sharafdg.com/product/1214793/playstation-network-live-usd-5-online-gift-card/"))
