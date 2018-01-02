import requests
from bs4 import BeautifulSoup
import pickle
import os
import xlsxwriter
from random import randint
from random import shuffle
from user_agent import generate_user_agent
import time
import grequests

# from openpyxl import Workbook

# sudo docker run -p 5023:5023 -p 8050:8050 -p 8051:8051 scrapinghub/splash --max-timeout 120

UK_identifiers = ('UK','Great Britain', 'GB', 'United Kingdom')

def open_proxies_list():
	with open('proxies_http.txt','r') as f:
		proxies = f.readlines()

	stripped_proxies = []

	for proxy in proxies:
		proxy = proxy.strip()
		stripped_proxies.append(proxy)

	return stripped_proxies

def random_proxy():
	proxies_list = open_proxies_list()
	index = randint(0,len(proxies_list)-1)
	proxy = {'http' : proxies_list[index]}
	return proxy

def search_strings():
	f = open('words.txt','r')
	search_strings = f.read()
	f.close
	search_strings = search_strings.split()
	shuffle(search_strings)
	return search_strings

def soupify_search_page(search_string):

	proxy = random_proxy()
	user_agent = generate_user_agent()
	headers = {'User-Agent': user_agent}
	print user_agent
	print proxy

	query_url = "https://www.amazon.co.uk/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords="+ search_string
	try:
		rendered_html = requests.get(query_url, headers = headers, proxies = proxy)
		soup = BeautifulSoup(rendered_html.text, "html.parser")
	except requests.ConnectionError as e:
		print e
		rendered_html = requests.get(query_url,headers = headers, proxies = proxy)
		soup = BeautifulSoup(rendered_html.text, "html.parser")
	if 'captcha' in soup.text:
		print "CAPTCHA! Rendering failed!"
		# time.sleep(60)
		return False

	print "search results page rendered successfully: " + str(rendered_html.ok)
	return soup

# def soupify_page(next_page_url):

# 	proxy = random_proxy()
# 	user_agent = generate_user_agent()
# 	headers = {'User-Agent': user_agent}

# 	try:
# 		request_url = requests.get(next_page_url, headers = headers, proxies = proxy,timeout=5)
# 		rendered_html = requests.get(request_url.url, headers = headers, proxies = proxy)
# 		soup = BeautifulSoup(rendered_html.text, "html.parser")
# 	except requests.ConnectionError as e:
# 		print "connection error!"
# 		print e
# 		request_url = requests.get(next_page_url, headers = headers, proxies = proxy, timeout=5)
# 		rendered_html = requests.get(request_url.url, headers = headers, proxies = proxy, timeout=5)
# 		soup = BeautifulSoup(rendered_html.text, "html.parser")
# 	except requests.ProxyError as e:
# 		print "proxy error!"
# 		soupify_page(next_page_url)

# 	print "page rendered successfully: " + str(rendered_html.ok)
# 	return soup


def soupify_page_recoursively(next_page_url):

	proxy = random_proxy()
	user_agent = generate_user_agent()
	headers = {'User-Agent': user_agent}
	print user_agent
	print proxy

	try:
		request_url = requests.get(next_page_url, headers = headers, proxies = proxy,timeout=5)
		rendered_html = requests.get(request_url.url, headers = headers, proxies = proxy)
		soup = BeautifulSoup(rendered_html.text, "html.parser")
	except requests.ConnectionError as e:
		print "connection error!"
		return soupify_page_recoursively(next_page_url)
	except Exception as e:
		print "some error!"
		return soupify_page_recoursively(next_page_url)
	if 'captcha' in soup.text:
		print "CAPTCHA! Rendering failed!"
		# time.sleep(60)
		return False
		# return soupify_page_recoursively(next_page_url)
	print "page rendered successfully: " + str(rendered_html.ok)
	return soup

def find_next_page_button(soup_page):
	
	try:
		next_page = soup_page(class_="pagnNext")[0]['href'] 
		next_page = 'https://www.amazon.co.uk' + str(next_page)
	except IndexError as e:
		print "no next button"
		return False

	return next_page

def scrap_links_from_page(soup_page):

	products_links = []

	try: 
		prodlist = soup_page(class_='s-result-item celwidget ')

		if prodlist:
			try:
				for item in prodlist:
					if "http" not in item.a['href']:
						print "*"*10+'skipping redirect links'+"*"*10
					elif "slredirect" in item.a['href']:
						print "*"*10+'skipping redirect links'+"*"*10
					else:
						products_links.append(item.a['href'])
			except Exception as e:
				print "a problem with collecting product links from search results"
				print e
				return False
		else:
			print "no product links"
			return False

		return products_links
	except:
		print "no product links"
		return False


def products_links_file_name(search_string):
	products_folder_path = '/home/ostap/Documents/programming/Saad1/products_lists'
	short_file_name = 'products_links_amazon_{}'.format(search_string)
	complete_file_name = os.path.join(products_folder_path,short_file_name)
	return short_file_name, complete_file_name

def save_products_links_file(search_string, products_links):
	with open (products_links_file_name(search_string)[1], 'w') as f:
		pickle.dump(products_links, f)

def sellers_list_file_name(search_string):

	short_file_name = 'sellers_details_amazon_{}'.format(search_string)
	sellers_folder_path = '/home/ostap/Documents/programming/Saad1/sellers_lists'
	complete_file_name = os.path.join(sellers_folder_path,short_file_name)
	return short_file_name, complete_file_name

def save_sellers_list_file(search_string, sellers_list):
	with open (sellers_list_file_name(search_string)[1], 'w') as f:
		pickle.dump(sellers_list, f)

def save_products_links(search_string):

	products_links = []

	page = soupify_search_page(search_string)

	if page:

		links = scrap_links_from_page(page)

		if links:
			for link in links:
				products_links.append(link)

			next_page = find_next_page_button(page)
			while True:
				if next_page:		
					page = soupify_page_recoursively(next_page)
					links = scrap_links_from_page(page)
					if links:
						for link in links:
							products_links.append(link)
						next_page = find_next_page_button(page)
						print next_page
					else:
 						break
				else:
					"*"*10+"no NEXT page. End of search results reached"+"*"*10
					break

			save_products_links_file(search_string, products_links)
			return products_links_file_name(search_string)

		else:
			print "no matches for " + search_string
			return False
	else:
		print "no matches for " + search_string
		return False


def open_product_urls_file(file_name):
	''' 
	takes product of save_products_links(search_string) 
	'''
	try:
		with open (file_name,'a+') as f:
			products_links = pickle.load(f)
			return products_links
	except Exception as e:
		print e
	# except EOFError as e:
		print "*"*10+"no product links file found for "+search_string+"*"*10
		return False

def get_products_urls(search_string):

	products_links = []
	file_name = save_products_links(search_string)

	if file_name:
		products_links = open_product_urls_file(file_name[1])
		return products_links
	else:
		print "*"*10+"no product links file found for "+search_string+"*"*10
		return False	

def list_of_pack_of_urls(product_urls):

	list_of_pack_of_urls = []

	pack_of_urls = set()

	for url in product_urls:
		if product_urls.index(url) < len(product_urls)-1:
			if len(pack_of_urls) < 2:
				pack_of_urls.add(url)
			else:
				list_of_pack_of_urls.append(pack_of_urls)
				pack_of_urls = set()
		else:
			pack_of_urls.add(url)
			list_of_pack_of_urls.append(pack_of_urls)
			return list_of_pack_of_urls

	return list_of_pack_of_urls

def get_list_of_packs_of_product_pages(list_of_packs_of_product_urls):
	list_of_product_pages = []
	for pack_of_urls in list_of_packs_of_product_urls:
		pack_of_product_pages = get_pack_of_soup_product_pages_async(pack_of_urls)
		list_of_product_pages.append(pack_of_product_pages)
	return list_of_product_pages

def clean_responses(final_request_urls):
	final_request_urls = final_request_urls
	result = []
	for response in final_request_urls:
		if response is None:
			pass
		else:
			result.append(response)

	return result

def get_pack_of_soup_product_pages_async(urls):

	print "sending a pack of async requests!"
	rendered_urls = {grequests.get(u,proxies=random_proxy(),headers ={'User-Agent': generate_user_agent()}) for u in urls}
	time.sleep(random.randint(1,5))
	soup_rendered_urls = grequests.map(rendered_urls)
	soup_rendered_urls = clean_responses(soup_rendered_urls)

	return soup_rendered_urls

def get_sellers_details(page):

	global result 

	def seller_names_iterator(result):
		for item in result:
			yield item['seller-name']

	seller_names_iterator = seller_names_iterator(result)

	soup = soupify_page_recoursively(page.url)
	print "*"*10+"processing"+"*"*10 + page.url

	if soup:
		try:
			seller_link = 'https://www.amazon.co.uk' + soup(id='merchant-info')[0].a['href']

			if seller_link:
				print "*"*10+"seller link found" +"*"*10
				print seller_link
				"*"*10+"starting soupification"+"*"*10
				seller_page = soupify_page_recoursively(seller_link)
				"*"*10+"soupified successfully!"+"*"*10
				seller_name = seller_page(id='sellerName')[0].text
				print 'seller name is ' + seller_name

				if seller_name not in seller_names_iterator:
					print "*"*10+"seller is unique!"+"*"*10
					try:
						seller_information_box = seller_page('ul',class_='a-unordered-list a-nostyle a-vertical')[0]
						print "*"*10+"information box is found"+"*"*10
					except Exception as e:
						print e
						print "*"*10+"information box is not found"+"*"*10
						return False
					phone, address_box = get_phone_and_address_box(seller_information_box)
					country = address_box('li')[-1].text
					print country

					for UK in UK_identifiers:							
						if UK in country:
							print "*"*10+"YEY! seller is IN the UK" +"*"*10
							
							postcode = address_box('li')[-2].text
							print "*"*10+"postcode found" +"*"*10
							feedback_box = seller_page(id='feedback-summary-table')[0]
							print "*"*10+"feedback box found" +"*"*10
							feedback_count_raw = feedback_box('tr')[4]
							result.append({
							'seller-name' : seller_name,
							'seller-postcode' : postcode,
							'seller-phone' : phone, 
							'seller-address' : get_address(address_box),
							'thrity-days-count' : str(feedback_count_raw(class_='a-text-right')[0].text),
							'sixty-days-count' : str(feedback_count_raw(class_='a-text-right')[1].text),
							'twelwe-month-count' : str(feedback_count_raw(class_='a-text-right')[2].text),
							'lifetime-count' : str(feedback_count_raw(class_='a-text-right')[3].text)
							})
							print "*"*10+"YEY! Information has been successfully appended!" +"*"*10
							return True
						else: 
							print "*"*10+"seller is not in the UK" +"*"*10
							return False
				else: 
					print "*"*10+"seller name is already collected" +"*"*10
					return False
			else:
				print "*"*10+"seller link not found" +"*"*10
				return False
		except TypeError as e:
			print "*"*10+"seller link not found" +"*"*10
			return False
		except IndexError as e:
			print "*"*10+"seller link not found" +"*"*10
			return False
	else:
		return False

def get_phone_and_address_box(seller_information_box):

	address_box = None
	phone = None

	for li in seller_information_box('li'):
		if 'phone' in li.text.lower():
			phone = li.text
		elif 'business address:' in li.text.lower():
			address_box = li

	if phone == None:
		phone = "no phone provided"
	return phone, address_box

def get_address(address_box):

	address_box('li')[-1].extract()
	address_box('li')[-1].extract()
	address_list = []

	for li in address_box('li'):
		address_list.append(li.text)

	address = ", ".join(address_list)

	return address

def calculate_hits():

	f = open ('final_sellers_list_amazon','r')
	contents = pickle.load(f)
	hits = len(contents)
	f.close()

	return hits

def load_final_results():

	saved_results = []

	if 'final_sellers_list_amazon' in os.listdir('.'):
		print '**********final list found**********'
		f = open ('final_sellers_list_amazon', 'r')
		saved_results = pickle.load(f)
		f.close()
		
	return saved_results

def merge_hits():

	sellers_folder_path = '/home/ostap/Documents/programming/Saad1/sellers_lists'
	results = []

	for filename in os.listdir('/home/ostap/Documents/programming/Saad1/sellers_lists'):
		complete_file_name = os.path.join(sellers_folder_path,filename)
		f = open (complete_file_name,'r')
		contents = pickle.load(f)	
		for item in contents:
			results.append(item)
		f.close()
		os.remove(complete_file_name)

	saved_results = load_final_results()

	for result in results:
		saved_results.append(result)

	f = open('final_sellers_list_amazon','w')
	pickle.dump(saved_results, f)
	f.close()

def remove_duplicates():
	with open ('final_sellers_list_amazon', 'a+') as f:
		results = pickle.load(f)
		print str(len(results))
		indexes = len(results)
		for i in range(indexes-2):
			print i
			try:
				for j in range(indexes)[i+1:]:
					if results[i]['seller-name'] == results[j]['seller-name']:
						print results[j]['seller-name']
						results.pop(j)
			except IndexError as e:
				print e
				continue
		pickle.dump(results, f)

def make_xlsx_file():

	workbook = xlsxwriter.Workbook('sellers-list-amazon.xlsx')
	worksheet = workbook.add_worksheet()
	sellers = load_final_results()

	row = 0
	for seller in sellers:
		worksheet.write(row, 1, seller['seller-name'])
		worksheet.write(row, 2, seller['seller-phone'])
		worksheet.write(row, 3, seller['seller-postcode'])
		worksheet.write(row, 4, seller['seller-address'])
		worksheet.write(row, 5, seller['thrity-days-count'])
		worksheet.write(row, 6, seller['sixty-days-count'])
		worksheet.write(row, 7, seller['twelwe-month-count'])
		worksheet.write(row, 8, seller['lifetime-count'])
		row+=1

	workbook.close()

def get_many_sellers(how_many):

	for search_string in search_strings():
		result = []
		global result
		print "*"*10 + search_string + "*"*10
		product_urls = get_products_urls(search_string)
		if product_urls:
			list_of_packs_of_product_urls = list_of_pack_of_urls(product_urls)
			list_of_packs_of_product_pages = get_list_of_packs_of_product_pages(list_of_packs_of_product_urls)
			counter = 1
			for pack_of_product_pages in list_of_packs_of_product_pages:
				for page in pack_of_product_pages:
					get_sellers_details(page)
			
			save_sellers_list_file(search_string,result)
			merge_hits()
			hits = calculate_hits()
			print "*"*10 + str(hits) + "*"*10

			if hits >= how_many:
				break

		else:
			continue

	merge_hits()
	print "hits merged"
	remove_duplicates()
	print "duplicates removed"
	make_xlsx_file()
	print "excel file created"

if __name__=="__main__":
	get_many_sellers(200)

# def Excel():
# 	wb = Workbook()
# 	ws = wb.active
# 	for row in ws.iter_rows(max_col=5):