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

result = {'hits': [], 'count': 0}

headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}

def search_strings():
	f = open('words.txt','r')
	search_strings = f.read()
	f.close
	search_strings = search_strings.split()
	return search_strings

def soupify_search_page(search_string):

	query_url = "http://www.ebay.com/sch/i.html?_nkw="+ search_string+"&_in_kw=1&_ex_kw=&_sacat=0&_udlo=&_udhi=&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=&_sargn=-1%26saslc%3D1&_fsradio2=%26LH_LocatedIn%3D1&_salic=3&LH_SubLocation=1&_sop=12&_dmd=1&_ipg=200"
	try:
		rendered_html = requests.get(query_url)
		soup = BeautifulSoup(rendered_html.text, "html.parser")
	except requests.ConnectionError as e:
		print e
		rendered_html = requests.get(query_url)
		soup = BeautifulSoup(rendered_html.text, "html.parser")
	return soup

def soupify_page(next_page_url):

	try:
		request_url = requests.get(next_page_url)
		rendered_html = requests.get(request_url.url)
		soup = BeautifulSoup(rendered_html.text, "html.parser")
	except requests.ConnectionError as e:
		print e
		request_url = requests.get(next_page_url)
		rendered_html = requests.get(request_url.url)
		soup = BeautifulSoup(rendered_html.text, "html.parser")
	return soup

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

def soupify_page_recoursively(next_page_url):

	user_agent = generate_user_agent()
	headers = {'User-Agent': user_agent}

	try:
		request_url = requests.get(next_page_url, headers = headers,timeout=5)
		rendered_html = requests.get(request_url.url, headers = headers)
		soup = BeautifulSoup(rendered_html.text, "html.parser")
	except requests.ConnectionError as e:
		print "connection error!"
		return soupify_page_recoursively(next_page_url)
	except Exception as e:
		print e
		return soupify_page_recoursively(next_page_url)
	if 'captcha' in soup.text:
		print "CAPTCHA! Rendering failed! Sleep 10 sec and restart!"
		time.sleep(60)
		return soupify_page_recoursively(next_page_url)
	print "page rendered successfully: " + str(rendered_html.ok)
	return soup


def find_next_page_button(soup_page):
	
	try:
		next_page = soup_page(class_="gspr next")[0]['href'] 
	except IndexError as e:
		print "no next button"
		return None

	return next_page

def scrap_links_from_page(soup_page):

	products_links = []

	prodlist = soup_page(class_='sresult lvresult clearfix li shic')

	if prodlist:
		try:
			for item in prodlist:
				products_links.append(item.a['href'])
		except:
			pass
	else:
		print "no product links"
		return None

	return products_links


def products_links_file_name(search_string):
	products_folder_path = '/home/ostap/Documents/programming/Saad/products_lists'
	short_file_name = 'products_links_{}'.format(search_string)
	complete_file_name = os.path.join(products_folder_path,short_file_name)
	return short_file_name, complete_file_name

def save_products_links_file(search_string, products_links):
	with open (products_links_file_name(search_string)[1], 'w') as f:
		pickle.dump(products_links, f)

def sellers_list_file_name(search_string):

	short_file_name = 'sellers_details_{}'.format(search_string)
	sellers_folder_path = '/home/ostap/Documents/programming/Saad/sellers_lists'
	complete_file_name = os.path.join(sellers_folder_path,short_file_name)
	return short_file_name, complete_file_name

def save_sellers_list_file(search_string, sellers_list):
	with open (sellers_list_file_name(search_string)[1], 'w') as f:
		pickle.dump(sellers_list, f)

def save_products_links(search_string):

	products_links = []

	page = soupify_search_page(search_string)

	links = scrap_links_from_page(page)

	if links:
		for link in links:
			products_links.append(link)

		next_page = find_next_page_button(page)
		counter = 0
		while counter == 0:
			if next_page:		
				counter+=1
				print counter
				page = soupify_page_recoursively(next_page)
				links = scrap_links_from_page(page)
				if links:
					for link in links:
						products_links.append(link)
					next_page = find_next_page_button(page)
					print next_page
			else:
				"*"*10+"no NEXT page. End of search results reached"+"*"*10
				break

		save_products_links_file(search_string,products_links)
		return products_links_file_name(search_string)

	else:
		print "no matches for " + search_string
		return None


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
		return None

def get_products_urls(search_string):

	products_links = []
	file_name = save_products_links(search_string)

	if file_name:
		products_links = open_product_urls_file(file_name[1])
		return products_links
	else:
		print "*"*10+"no product links file found for "+search_string+"*"*10
		return None	

def list_of_pack_of_urls(product_urls):

	list_of_pack_of_urls = []

	pack_of_urls = set()

	for url in product_urls:
		if product_urls.index(url) < len(product_urls)-1:
			if len(pack_of_urls) < 5:
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
	request_urls = (grequests.get(u,proxies=random_proxy(),headers ={'User-Agent': generate_user_agent()}) for u in urls)
	final_request_urls = grequests.map(request_urls)
	final_request_urls = clean_responses(final_request_urls)
	rendered_urls = {grequests.get(u.url,proxies=random_proxy(),headers ={'User-Agent': generate_user_agent()}) for u in final_request_urls}
	time.sleep(3)
	soup_rendered_urls = grequests.map(rendered_urls)
	soup_rendered_urls = clean_responses(soup_rendered_urls)

	return soup_rendered_urls

def get_sellers_details(page):

	result = []


	def seller_names_iterator():
		for item in result:
			yield item['seller-name']

	product_page = soupify_page_recoursively(product_url.url)

	print "*"*10+"processing"+"*"*10 + product_url.url

	if product_page(id='bsi-c'):
		print "*"*10+"business seller information box found"+"*"*10
		try:
			if "United Kingdom" in product_page(class_='bsi-c1')[0].text:
				if product_page(class_='bsi-bn')[0].text not in seller_names_iterator():
					if product_page('span', class_='bsi-lbl')[0].text == 'Phone:':
						print "*"*10+"phone found*"+"*"*10
						phone = product_page('span', class_='bsi-lbl')[0].next_sibling.text
						print phone
						seller_url = product_page(class_='mbg vi-VR-margBtm3')[0].a['href'] 
						print "seller url is " + seller_url
						seller_page = soupify_page_recoursively(seller_url)
						email_box = seller_page(class_='bsi_table')[0]
						address_box = product_page(class_='bsi-c1')[0]
						postcode = address_box('div')[-2].text
						address = get_address(address_box)
						all_feed_back_url = seller_page(class_='all_fb fr')[0].a['href']
						all_feed_back_page = soupify_page_recoursively(all_feed_back_url) 
						feedback_box = all_feed_back_page(class_='frp')[0]
						feedback_count_raw = feedback_box(class_='fbsSmallYukon')[0]
						result.append({
						'seller-name': product_page(class_='bsi-bn')[0].text,
						'seller-url': seller_url,
						'seller-address': address,
						'seller-phone': phone,
						'category' : product_page(class_='bc-w')[0].text,
						'seller-postcode' : postcode,
						'seller-email': email_box(class_='bsi_cell_value')[-1].text,
						'seller-date-of-registration' : seller_page('span', string='Member since: ')[0].parent('span')[1].text,
						'thrity-days-count' : str(feedback_count_raw(id="RFRId")[0].text),
						'six-months-count' : str(feedback_count_raw(id="RFRId")[2].text),
						'twelwe-month-count' : str(feedback_count_raw(id="RFRId")[4].text),
						'all-feedback-count' : str(all_feed_back_page(class_='mbg-l')[0].text)})
						print "results appended!"


					else:
						print "*"*10+"phone not found"+"*"*10
				else: print "*"*10+"seller is already saved"+"*"*10
			else: print "*"*10+"not in United Kingdom"+"*"*10
		except IndexError as e:
			print e
	else: "business seller information box found"

	save_sellers_list_file(search_string,result)
	return True

def get_address(address_box):

	address_box('div')[-1].extract()
	address_box('div')[-1].extract()
	address_list = []

	for div in address_box('div'):
		address_list.append(div.text)

	address = ", ".join(address_list)

	return address

def calculate_hits():

	f = open ('final_sellers_list','r')
	contents = pickle.load(f)
	hits = len(contents)
	f.close()

	return hits

def load_final_results():

	saved_results = []

	if 'final_sellers_list' in os.listdir('.'):
		print '**********final list found**********'
		f = open ('final_sellers_list', 'r')
		saved_results = pickle.load(f)
		f.close()
		
	return saved_results

def merge_hits():

	sellers_folder_path = '/home/ostap/Documents/programming/Saad/sellers_lists'
	results = []

	for filename in os.listdir('/home/ostap/Documents/programming/Saad/sellers_lists'):
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

	f = open('final_sellers_list','w')
	pickle.dump(saved_results, f)
	f.close()

def remove_duplicates():
	with open ('final_sellers_list', 'a+') as f:
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

	workbook = xlsxwriter.Workbook('sellers-list.xlsx')
	worksheet = workbook.add_worksheet()
	sellers = load_final_results()

	row = 0
	for seller in sellers:
		worksheet.write(row, 1, seller['seller-name'])
		worksheet.write(row, 2, seller['seller-phone'])
		worksheet.write(row, 3, seller['seller-postcode'])
		worksheet.write(row, 4, seller['seller-address'])
		worksheet.write(row, 5, seller['thrity-days-count'])
		worksheet.write(row, 6, seller['six-months-count'])
		worksheet.write(row, 7, seller['twelwe-month-count'])
		worksheet.write(row, 8, seller['all-feedback-count'])
		worksheet.write(row, 9, seller['seller-url'])
		worksheet.write(row, 10, seller['seller-email'])
		worksheet.write(row, 11, seller['seller-date-of-registration'])
		worksheet.write(row, 12, seller['category'])
		row+=1

	workbook.close()

def get_many_sellers(how_many):

	for search_string in search_strings():
		print "*"*10 + search_string + "*"*10
		product_urls = get_products_urls(search_string)
		if product_urls:
			list_of_packs_of_product_urls = list_of_pack_of_urls(product_urls)
			list_of_packs_of_product_pages = get_list_of_packs_of_product_pages(list_of_packs_of_product_urls)
			for pack_of_product_pages in list_of_packs_of_product_pages:
				for page in pack_of_product_pages:
					time.sleep(1)
					get_sellers_details(page)
					print "processing " + search_string
					if get_sellers_details(page):
						merge_hits()
						hits = calculate_hits()
						print "*"*10 + str(hits) + "*"*10
						if hits >= how_many:
							break
					else:
						continue
		else:
			continue

	merge_hits()
	print "hits merged"
	remove_duplicates()
	print "duplicates removed"
	make_xlsx_file()
	print "excel file created"



# def Excel():
# 	wb = Workbook()
# 	ws = wb.active
# 	for row in ws.iter_rows(max_col=5):