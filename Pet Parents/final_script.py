from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
import requests
from bs4 import BeautifulSoup
import csv
import time
import json
import xlsxwriter


class Master_quiz_selector():

	def __init__(self, browser):

		self.browser = browser
		self.icons_add_btns = self.browser.find_elements_by_class_name('icon-add')
		self.children_add_btn = self.icons_add_btns[0]
		self.dogs_add_btn = self.icons_add_btns[1]
		self.results_btn = self.browser.find_elements_by_class_name('show-me-matches')[3]
		self.decrease_vol_btn = self.browser.find_elements_by_class_name('icon-subtract')[2]
		self.increase_vol_btn = self.icons_add_btns[2]
		self.results_btn = self.browser.find_elements_by_class_name('show-me-matches')[3]

		self.zip_form = self.browser.find_element_by_name("zipcode")
		self.zipcodes = self.zipcodes()
		self.accomodation_btns = self.browser.find_elements_by_tag_name('label')[:2]
		self.children_dogs_btns = self.children_dogs_btns_generator()
		self.activities_btns = self.browser.find_elements_by_tag_name('label')[2:5]
		self.vol_btns = self.vol_btns_generator()
		self.cleanliness_btns = self.browser.find_elements_by_tag_name('label')[5:8]
		self.continue_buttons = self.browser.find_elements_by_class_name('cont-btn')
		self.back_buttons = self.browser.find_elements_by_css_selector('.back-btn.hide-on-tablet-up')

	def zipcodes(self):

		url = "http://www.phaster.com/zip_code.html"
		page = requests.get(url)
		soup = BeautifulSoup(page.text)
		trs = soup('tr')[1:-1]
		zip_cells = [i('td')[2].text for i in trs]

		zip_cells_formatted = []
		for s in zip_cells:
			x = s.replace('thru', ' ')
			x = x.replace('-', ' ')
			x = x.replace('   ', ' ')
			zip_cells_formatted.append(x)

		str_zip_cells = [i.split(u'\xa0') if u'\xa0' in i else i for i in zip_cells_formatted]

		last = [i.split(' ') if type(i) is unicode else [z.split(' ') for z in i] if type(i) is list else i for i in str_zip_cells]

		last_last = sum(last, [])

		for i in last_last:
			if type(i) is list:
				for x in i:
					last_last.append(x)
				last_last.pop(last_last.index(i))

		for i in last_last:
			if type(i) is list:
				for x in i:
					last_last.append(x)
				last_last.pop(last_last.index(i))


		set_zips = set(last_last)
		set_zips.remove(u'')
		list_zips = list(set_zips)

		return list_zips

	def	children_dogs_btns(self, cd_counter):

		if cd_counter == 0:
			result = {'children_clicks':0,'dogs_clicks':0}
			return result
		elif len(str(cd_counter)) < 2:
			result = {'children_clicks':0,'dogs_clicks':cd_counter}
			return result
		else:
			str_cd_counter = str(cd_counter)
			child_clicks = int(str_cd_counter[0])
			dog_clicks = int(str_cd_counter[1])
			result = {'children_clicks':child_clicks,'dogs_clicks':dog_clicks}
			return result

	def children_dogs_btns_generator(self):

		def counter():
			for i in range(45):
				if i < 5:
					yield i
				elif len(str(i)) == 2 and int(str(i)[1]) < 5:
					yield i
		result = []

		counter = counter()

		for i in counter:
			result.append(self.children_dogs_btns(i))

		return result

	def vol_btns(self, vol_counter):

		decrease_vol_btn = self.browser.find_elements_by_class_name('icon-subtract')[2]
		increase_vol_btn = self.browser.find_elements_by_class_name('icon-add')[2]
		vol_btns = []
		vol_btns.append(decrease_vol_btn)
		vol_btns.append(increase_vol_btn)

		if vol_counter <=4:
			return vol_counter
		elif 4 < vol_counter <= 8:
			return vol_counter*-1 

	def vol_btns_generator(self):
		result = []

		i = 0
		while i <=8:
			result.append(self.vol_btns(i))
			i+=1
		return result

class Small_quiz_selector(Master_quiz_selector):

	def __init__(self, browser, zipcode=None, accomodation_type=None, children=None, dogs=None, activity=None, volume=None, cleanliness=None):
		Master_quiz_selector.__init__(self, browser)
		self.zipcode=zipcode
		self.accomodation_type=self.find_btn_by_text(accomodation_type)
		self.children_dogs={'children_clicks': children, 'dogs_clicks': dogs}
		self.activity=self.find_btn_by_text(activity)
		self.volume=volume
		self.cleanliness=self.find_btn_by_text(cleanliness)


	def find_btn_by_text(self, btn_text):

		text = btn_text.split()

		if text[0] == u'a':
			text =  text[1].swapcase().capitalize()
		elif text[1] == u'TIDY':
			text = text[0]
		else:
			text = text[-1].swapcase().capitalize()

		btn = self.browser.find_element_by_xpath("//*[contains(text(), '"+text+"')]")
		return btn 

class Administartor():

		def __init__(self, master_quiz_selector, spider):
			self.master_quiz_selector = master_quiz_selector
			self.result = []
			self.spider = spider

		def center_on_button(self, browser, btn):

			browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(3)

			location_x = btn.location['x']
			location_y = btn.location['y']
			
			browser.execute_script("window.scrollTo(0, %d);" %location_x)
			browser.execute_script("window.scrollTo(0, %d);" %location_y)

			i = ActionChains(browser).move_to_element(btn)
			i.perform()

		def center_on_button_and_click(browser, self, btn):
			ActionChains(browser).move_to_element(btn).click().perform()	

		def route(self):

			for zipcode in self.master_quiz_selector.zipcodes[:1]:
				for acmd in self.master_quiz_selector.accomodation_btns:
					self.center_on_button(master_quiz_selector.browser, acmd)
					acmd_text = acmd.text.replace('\n',' ')
					for children_dogs in self.master_quiz_selector.children_dogs_btns:
						for activity_btn in self.master_quiz_selector.activities_btns:
							self.center_on_button(master_quiz_selector.browser, activity_btn)
							activity_text = activity_btn.text.replace('\n',' ')
							for vol_btn in self.master_quiz_selector.vol_btns:
								for clns in self.master_quiz_selector.cleanliness_btns:
									self.center_on_button(master_quiz_selector.browser, clns)
									clns_text = clns.text.replace('\n',' ')
									selections = dict()
									selections.update({
										'zipcode': zipcode,
										'accomodation_type':acmd_text,
										'children': children_dogs['children_clicks'],
										'dogs': children_dogs['dogs_clicks'],
										'activity': activity_text,
										'volume': vol_btn,
										'cleanliness': clns_text})
									yield selections

		def start(self):
		
			routes = self.route()

			for route in routes:

				browser = webdriver.Chrome()
				browser.get(query_url)
				time.sleep(5)

				small_quiz_selector = Small_quiz_selector(browser, **route)
				dogs = self.run_spider(small_quiz_selector)
				result = []
				result.append(route)
				result.append(dogs)
				self.result.append(result)

				browser.close()


		def run_spider (self, small_quiz_selector):

			self.center_on_button(small_quiz_selector.browser, small_quiz_selector.zip_form)
			small_quiz_selector.zip_form.send_keys(small_quiz_selector.zipcode)
			time.sleep(2)
			self.spider.click_button(small_quiz_selector.continue_buttons[0])
			time.sleep(1)

			self.spider.click_button(small_quiz_selector.accomodation_type)
			self.spider.click_button(small_quiz_selector.continue_buttons[1])

			self.spider.click_button(small_quiz_selector.children_dogs)
			time.sleep(1)
			self.spider.click_button(small_quiz_selector.continue_buttons[2])
			time.sleep(1)

			self.spider.click_button(small_quiz_selector.activity)
			self.spider.click_button(small_quiz_selector.continue_buttons[3])
			time.sleep(1)

			self.spider.click_button(small_quiz_selector.volume, small_quiz_selector)
			self.spider.click_button(small_quiz_selector.continue_buttons[4])
			time.sleep(1)

			self.spider.click_button(small_quiz_selector.cleanliness)
			self.spider.click_button(small_quiz_selector.results_btn)
			time.sleep(1)
			dogs = self.spider.process_results_page(small_quiz_selector.browser)

			return dogs

		def make_xlsx_file(self):

			workbook = xlsxwriter.Workbook('Pet_Parents_results.xlsx')
			worksheet = workbook.add_worksheet()

			results = self.result

			worksheet.write_string(0, 1, 'zipcode')
			worksheet.write_string(0, 2, 'accomodation_type')
			worksheet.write_string(0, 3, 'children')
			worksheet.write_string(0, 4, 'dogs')
			worksheet.write_string(0, 5, 'activity')
			worksheet.write_string(0, 6, 'volume')
			worksheet.write_string(0, 7, 'cleanliness')

			g = 1
			for cell in range(1,6):
				i = 8*g		
				worksheet.write_string(0, i+1, 'dog ' + str(cell) + ' name')
				worksheet.write_string(0, i+2, 'dog ' + str(cell) + ' description')
				worksheet.write_string(0, i+3, 'dog ' + str(cell) + ' size')
				worksheet.write_string(0, i+4, 'dog ' + str(cell) + ' coat')
				worksheet.write_string(0, i+5, 'dog ' + str(cell) + ' trainability')
				worksheet.write_string(0, i+6, 'dog ' + str(cell) + ' grooming required')
				worksheet.write_string(0, i+7, 'dog ' + str(cell) + ' activity level')
				worksheet.write_string(0, i+8, 'dog ' + str(cell) + ' barking level')
				g+=1

			row = 1
			for result in results:
				worksheet.write_string(row, 1, result[0]['zipcode'])
				worksheet.write_string(row, 2, result[0]['accomodation_type'])
				worksheet.write(row, 3, result[0]['children'])
				worksheet.write(row, 4, result[0]['dogs'])
				worksheet.write_string(row, 5, result[0]['activity'])
				worksheet.write(row, 6, result[0]['volume'])
				worksheet.write_string(row, 7, result[0]['cleanliness'])
				g = 1
				for dog in result[1]:
					i = 8*g		
					worksheet.write_string(row, i+1, dog['name'])
					worksheet.write_string(row, i+2, dog['description'])
					worksheet.write_string(row, i+3, dog['size'])
					worksheet.write_string(row, i+4, dog['coat'])
					worksheet.write_string(row, i+5, dog['trainability'])
					worksheet.write_string(row, i+6, dog['grooming required'])
					worksheet.write_string(row, i+7, dog['activity level'])
					worksheet.write_string(row, i+8, dog['barking level'])
					g+=1
				row+=1

			workbook.close()

class Spider():

	def click_button(self, btn, small_quiz_selector=None):

		small_quiz_selector = small_quiz_selector

		if type(btn) == dict:
			dogs_clicks = btn['dogs_clicks']
			children_clicks = btn['children_clicks']
			for click in range(dogs_clicks):
				small_quiz_selector.dogs_add_btn.click()
			for click in range(children_clicks):
				small_quiz_selector.children_add_btn.click()
		elif type(btn) == int:
			if btn>0:
				for click in range(btn):
					small_quiz_selector.increase_vol_btn.click()
			if btn<0:
				for click in range(btn*-1):
					small_quiz_selector.decrease_vol_btn.click()
		else:
			btn.click()

	def process_results_page(self, browser):

		soup = BeautifulSoup(browser.page_source)
		results_table = soup(class_='results-grid-swiper')

		dogs = soup(class_='result-dog')

		results = []

		for dog in dogs:
			dog_dict = dict()
			dog_dict.update({
				'name' : dog.h3.text,
				'description' : dog(class_='callout')[0].text,
				'size' : dog('li')[0].text.replace('size',''),
				'coat' : dog('li')[1].text.replace('coat length', ''),
				'trainability' : dog('li')[2].text.replace('trainability',''),
				'grooming required' : dog('li')[3].text.replace('grooming required',''),
				'activity level' : dog('li')[4].text.replace('activity level',''),
				'barking level' : dog('li')[5].text.replace('barking level','')})
			results.append(dog_dict)

		return results

if __name__ == '__main__':

	query_url = "http://www.akc.org/find-a-match/#slide1"
	master_browser = webdriver.Chrome()
	master_browser.get(query_url)
	master_quiz_selector = Master_quiz_selector(master_browser)
	spider = Spider()
	admin = Administartor(master_quiz_selector, spider)
	admin.start()
	admin.make_xlsx_file(spider)


# html = browser.page_source
# path = 'file://' + os.getcwd() + '/results.html
# '
# with open('results.html','w') as f:
# 	json.dump(html,f)

# browser1 = webdriver.Chrome()
# browser1.get(query_url)



# 	spider.click(quiz_selector.back_buttons[0])



	# def run(self,quiz_selector, spider):

	# def create_spider(self, **route):

	# 		query_url = "http://www.akc.org/find-a-match/#slide1"
	# 		browser = webdriver.Chrome()
	# 		browser.get(query_url)