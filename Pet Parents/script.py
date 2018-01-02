from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import csv

# zipcodes = []

# with open ('free-zipcode-database-Primary.csv') as csvfile:
# 	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
# 	for row in reader:
# 		zipcodes.append(row[0])


query_url = "http://www.akc.org/find-a-match/#slide1"

browser = webdriver.Chrome()
browser.get(query_url)

class Quiz_selector:

	cd_counter = 0
	vol_counter = 0
	icons_add_btns = browser.find_elements_by_class_name('icon-add')
	children_add_btn = icons_add_btns[0]
	dogs_add_btn = icons_add_btns[1]
	results_btn = browser.find_elements_by_class_name('show-me-matches')[3]
	decrease_vol_btn = browser.find_elements_by_class_name('icon-subtract')[2]
	increase_vol_btn = icons_add_btns[2]
	results_btn = browser.find_elements_by_class_name('show-me-matches')[3]

	def __init__(self):

		self.zipcodes = self.zipcodes()
		self.accomodation_btns = browser.find_elements_by_tag_name('label')[:2]
		self.children_dogs_btns = self.chlidren_dogs_btns_generator()
		self.activities_btns = browser.find_elements_by_tag_name('label')[2:5]
		self.vol_btns = self.vol_btns_generator()
		self.cleanliness_btns = browser.find_elements_by_tag_name('label')[5:8]
		self.continue_buttons = browser.find_elements_by_class_name('cont-btn')

		# self.zipcodes = self.zipcodes()
		# self.accomodation_btns = self.accomodation_btns()
		# self.activities_btns = self.activities_btns()
		# self.cleanliness_btns = self.cleanliness_btns()
		# self.continue_buttons = self.continue_buttons()
		# self.children_dogs_btns = self.chlidren_dogs_btns_generator()
		# self.vol_btns = self.vol_btns_generator()

	# def continue_buttons(self):

	# 	continue_buttons = browser.find_elements_by_class_name('cont-btn')

	# 	for btn in continue_buttons:
	# 		yield btn

	def zipcodes(self):
		zipcodes = []

		with open ('free-zipcode-database-Primary.csv') as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='"')
			for row in reader:
				zipcodes.append(row[0])
		return zipcodes

	# def	accomodation_btns(self):

	# 	types_of_accomodation = browser.find_elements_by_tag_name('label')[:2]

	# 	for btn in types_of_accomodation:
	# 		yield btn

	def	children_dogs_btns(self, cd_counter):

		if cd_counter = 0:
			result = {'children_clicks':0,'dogs_clicks':0}
			return result
		elif len(str(cd_counter)) < 2:
			result = {'children_clicks':0,'dogs_clicks':cd_counter}
			return result
		elif cd_counter <= 16:
			str_cd_counter = str(cd_counter)
			child_clicks = int(str_cd_counter[0])
			dog_clicks = int(str_cd_counter[1])
			result = {'children_clicks':child_clicks,'dogs_clicks':dog_clicks}
			return result

	def chlidren_dogs_btns_generator(self):
		result = []
		i = 0
		while i <= 16:
			result.append(children_dogs_btns(i))

		return result

	# def activities_btns(self):
		
	# 	types_of_activities = browser.find_elements_by_tag_name('label')[2:5]

	# 	for btn in types_of_activities:
	# 		yield btn

	def vol_btns(self, vol_counter):

		decrease_vol_btn = browser.find_elements_by_class_name('icon-subtract')[2]
		increase_vol_btn = browser.find_elements_by_class_name('icon-add')[2]
		vol_btns = []
		vol_btns.append(decrease_vol_btn)
		vol_btns.append(increase_vol_btn)

		if vol_counter <=4:
			return vol_counter
		elif 4 < vol_counter < 8:
			return vol_counter*-1 
		elif vol_counter = 8:
			return vol_counter*-1 

	def vol_btns_generator(self):
		result = []

		i = 0
		while i <=8:
			result.append(self.vol_btns(i))
		return result

	# def cleanliness_btns(self):

	# 	cleanliness = browser.find_elements_by_tag_name('label')[5:8]

	# 	for btn in cleanliness:
	# 		yield btn, results_btn

quiz_selector = Quiz_selector()
spider = Spider(quiz_selector)

for zipcode in quiz_selector.zipcodes:
	spider.click_button(zipcode)
	spider.click_button(next(quiz_selector.continue_buttons))
	for acmd in quiz_selector.accomodation_btns:
		spider.click_button(acmd)
		spider.click_button(next(quiz_selector.continue_buttons))
		for children_dogs in quiz_selector.chlidren_dogs_btns:
			spider.click_button(children_dogs)
			spider.click_button(next(quiz_selector.continue_buttons))
			for activity_btn in quiz_selector.activities_btns:
				spider.click_button(activity_btn)
				spider.click_button(next(quiz_selector.continue_buttons))
				for vol_btn in vol_btns:
					spider.click_button(vol_btn)
					spider.click_button(next(quiz_selector.continue_buttons))
					for clns in quiz_selector.cleanliness_btns:
						selections = dict()
						selections.update({
							'zipcode': zipcode,
							'accomodation_type':acmd.text.replace('\n',' '),
							'children': children_dogs['children_clicks'],
							'dogs': children_dogs['dogs_clicks'],
							'activity': activity_btn.text.replace('\n',' '),
							'volume': vol_btn,
							'cleanliness': clns.text.replace('\n',' ')})
						spider.click_button(clns)
						spider.click_button(results_btn)
						dogs = spider.process_results_page(selections)
						result = []
						result.append(selections)
						result.append(dogs)
						spider.results.append(result)
						selections = dict()

def make_xlsx_file(spider):

	workbook = xlsxwriter.Workbook('sellers-list-ebay.xlsx')
	worksheet = workbook.add_worksheet()

	results = spider.results

	worksheet.write_string(0, 1, 'zipcode')
	worksheet.write_string(0, 2, 'accomodation_type')
	worksheet.write_string(0, 3, 'children')
	worksheet.write_string(0, 4, 'dogs')
	worksheet.write_string(0, 5, 'activity')
	worksheet.write_string(0, 6, 'volume')
	worksheet.write_string(0, 7, 'cleanliness')

	row = 1
	for result in results:
		worksheet.write_string(row, 1, result['zipcode'])
		worksheet.write_string(row, 2, result['accomodation_type'])
		worksheet.write_string(row, 3, result['children'])
		worksheet.write_string(row, 4, result['dogs'])
		worksheet.write_string(row, 5, result['activity'])
		worksheet.write_string(row, 6, result['volume'])
		worksheet.write_string(row, 7, result['cleanliness'])
		i = 7
		g = 1
		for dogs in result[1]:
			i = i*g		
			worksheet.write(row, i+1, results[0]['name'])
			worksheet.write(row, i+2, results[0]['description'])
			worksheet.write(row, i+3, results[0]['size'])
			worksheet.write(row, i+4, results[0]['coat'])
			worksheet.write(row, i+5, results[0]['trainability'])
			worksheet.write(row, i+6, results[0]['grooming required'])
			worksheet.write(row, i+7, results[0]['activity level'])
			worksheet.write(row, i+8, results['barking level'])
			g+=1
		row+=1

	workbook.close()


spider.zipcode_select()
spider.accomodation_btns_click()
spider.children_dogs_btns_click()
spider.activities_btns_click()
spider.vol_btns_click()
spider.cleanliness_btns_click()

btns = [
quiz_selector.zipcodes,
quiz_selector.accomodation_btns,
quiz_selector.children_dogs_btns(quiz_selector.cd_counter),
quiz_selector.activities_btns,
quiz_selector.vol_btns(quiz_selector.vol_counter),
quiz_selector.cleanliness_btns,
]


class Spider(quiz_selector):

	results = []

	def click_button(btn):

		if type(btn) == dict:
			dogs_clicks = btn['dogs_clicks']
			children_clicks = btn['children_clicks']
			for click in range(dogs_clicks):
				dogs_add_btn.click()
			for click in range(children_clicks):
				children_add_btn.click()
		elif type(btn) == int:
			if btn>0:
				for click in range(btn):
					increase_vol_btn.click()
			if btn<0:
				for click in range(btn*-1):
					decrease_vol_btn.click()
		else:
			btn.click()

	def process_results_page(selections_dict):

		soup = BeautifulSoup(browser.page_source)
		results_table = soup(class_='results-grid-swiper')

		dogs = soup(class_='result-dog')

		results = []

		for dog in dogs:
			dog_dict = dict()
			dog_dict.update({
				'name' : dog.h3.text
				'description' : dog(class_='callout')[0].text
				'size' : dog('li')[0].text
				'coat' : dog('li')[1].text
				'trainability' : dog('li')[2].text
				'grooming required' : dog('li')[3].text
				'activity level' : dog('li')[4].text
				'barking level' : dog('li')[5].text]})
			results.append(dog_dict)

		return results

	def change_btn(btn):
		try:
			return next(btn)
		except StopIteration as e:
			print e


	def cleanliness_btns_click(self):
		btns = next(quiz_selector.cleanliness_btns)
		for btn in btns:
			btn.click()

	def zipcode_select(self):
		results = next(quiz_selector.zipcodes)
		zip_form = browser.find_element_by_name("zipcode")
		zip_form.send_keys(results[0])
		results[1].click()

	def accomodation_btns_click(self):
		btns = next(quiz_selector.accomodation_btns)
		for btn in btns:
			btn.click()

	def children_dogs_btns_click(self):
		result = quiz_selector.children_dogs_btns(quiz_selector.cd_counter)
		dogs_clicks = result['dogs_clicks']
		children_clicks = result['children_clicks']
		for click in range(dogs_clicks):
			dogs_add_btn.click()
		for click in range(children_clicks):
			children_add_btn.click()
		quiz_selector.cd_counter+=1


	def activities_btns_click(self):
		btns = next(quiz_selector.activities_btns)
		for btn in btns:
			btn.click()

	def vol_btns_click(self):
		result = quiz_selector.vol_btns(vol_btns.vol_counter)

		if result[0]>0:
			for click in range(result[0]):
				increase_vol_btn.click()
		if result[0]<0:
			for click in range(result[0]*-1):
				decrease_vol_btn.click()
		result[1].click()
		quiz_selector.vol_counter+=1

	def cleanliness_btns_click(self):
		btns = next(quiz_selector.cleanliness_btns)
		for btn in btns:
			btn.click()






zip_form = browser.find_element_by_name("zipcode")
zip_form.send_keys(zipcodes[0])
continue_buttons = browser.find_elements_by_class_name('cont-btn')
continue_buttons[0].click()

types_of_accomodation = browser.find_elements_by_tag_name('label')[:2]

home_button = types_of_accomodation[0]
apartment_button = types_of_accomodation[1]
home_button.click()
continue_buttons[1].click()

icons_add_btns = browser.find_elements_by_class_name('icon-add')
children_add_btn = icons_add[0]
dogs_add_btn = icons_add[1]
children_dogs = []
children_dogs.append(children_add_btn)
children_dogs.append(dogs_add_btn)
children_add_btn.click()
dogs_add_btn.click()
continue_buttons[2].click()

types_of_activities = browser.find_elements_by_tag_name('label')[2:5]
couch = types_of_activities[0] 
neighborhood = types_of_activities[1]
adventure = types_of_activities[2]

couch.click()
continue_buttons[3].click()

decrease_vol_btn = browser.find_elements_by_class_name('icon-subtract')[2]
decrease_vol_btn.click()
increase_vol_btn = icons_add_btns[2]
vol_btns = []
vol_btns.append(decrease_vol_btn)
vol_btns.append(increase_vol_btn)
increase_vol_btn.click()
continue_buttons[4].click()

cleanliness = browser.find_elements_by_tag_name('label')[5:8]
not_so = cleanliness[0]
occasionally = cleanliness[1]
supert = cleanliness[2]

results_btn = browser.find_elements_by_class_name('show-me-matches')[3]
results_btn.click()

soup = BeautifulSoup(browser.page_source)
results_table = soup(class_='results-grid-swiper')

dogs = soup(class_='result-dog')

name = dogs[0].h3.text
description = dogs[0](class_='callout')[0].text
size = dogs[0]('li')[0].text
coat = dogs[0]('li')[1].text
trainability = dogs[0]('li')[2].text
grooming required = dogs[0]('li')[3].text
activity level = dogs[0]('li')[4].text
barking level = dogs[0]('li')[5].text