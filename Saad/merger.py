import requests
from bs4 import BeautifulSoup
import cPickle as pickle
import os
import xlsxwriter
from random import randint
from random import shuffle
from user_agent import generate_user_agent
import time
import grequests
import re

def merge_hits():

	try:
		sellers_folder_path = '/home/ostap/Documents/programming/Saad/sellers_lists (another copy)'
		results = []

		for filename in os.listdir('/home/ostap/Documents/programming/Saad/sellers_lists (another copy)'):
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

		with open('/home/ostap/Documents/programming/Saad/final_sellers_list_ebay (4th copy)','w') as f:
			pickle.dump(saved_results, f)

		print "hits merged!"
	except Exception as e:
		print e
		time.sleep(5)
		merge_hits()

def load_final_results():

	try:

		saved_results = []

		if 'final_sellers_list_ebay (4th copy)' in os.listdir('/home/ostap/Documents/programming/Saad/'):
			print '**********final list found**********'
			f = open ('/home/ostap/Documents/programming/Saad/final_sellers_list_ebay (4th copy)', 'r')
			saved_results = pickle.load(f)
			f.close()
			
		return saved_results
	except EOFError as e:
		print e
		time.sleep(5)
		return load_final_results()
	except Exception as e:
		time.sleep(5)
		return load_final_results()

def make_xlsx_file():

	workbook = xlsxwriter.Workbook('/home/ostap/Documents/programming/Saad/sellers-list-ebay-15k.xlsx')

	categories = sellers_categories_set()

	for category in categories:
		category = re.sub('[\]\[:*\//?]', ' ', category)
		workbook.add_worksheet(category)

	sellers = load_final_results()

	sellers_by_categories = dict()

	for seller in sellers:
		category = re.sub('[\]\[:*\//?]', ' ', seller['category'])
		sellers_by_categories.setdefault(category,[]).append(seller)

	for key in sellers_by_categories:
		for seller in sellers_by_categories[key]:
			worksheet = workbook.get_worksheet_by_name(key)
			worksheet.write_string(0, 1, 'seller-name')
			worksheet.write_string(0, 2, 'seller-phone')
			worksheet.write_string(0, 3, 'seller-postcode')
			worksheet.write_string(0, 4, 'seller-address')
			worksheet.write_string(0, 5, 'thrity-days-count')
			worksheet.write_string(0, 6, 'six-months-count')
			worksheet.write_string(0, 7, 'twelwe-month-count')
			worksheet.write_string(0, 8, 'all-feedback-count')
			worksheet.write_string(0, 9, 'seller-url')
			worksheet.write_string(0, 10, 'seller-email')
			worksheet.write_string(0, 11, 'seller-date-of-registration')
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
			row+=1

	workbook.close()

def sellers_categories_set():

	sellers = load_final_results()

	sellers_categories = set()
	for seller in sellers:
		sellers_categories.add(seller['category'])

	return sellers_categories