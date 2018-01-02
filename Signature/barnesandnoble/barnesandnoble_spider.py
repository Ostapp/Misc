import scrapy
from barnesandnoble.items import EventItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.html import remove_tags
from datetime import datetime

class BarnesandnobleSpider(CrawlSpider):
	name = "events"

	pagination = 0

	start_urls = []

	if pagination > 0:

		for index in range(pagination):
			start_urls.append("https://stores.barnesandnoble.com/events?page="+str(index)+"&size=10&searchText=New+York%2c+NY+10024&month=Month&day=Day&type=AE&storeFilter=all&view=events&v="+str(index))
	else:

		start_urls.append("https://stores.barnesandnoble.com/events?searchText=New+York%2C+NY+10024&storeFilter=all&view=events&month=Month&day=Day&type=AE&sort=")

	rules = [Rule(LinkExtractor(allow='/event/9.*',restrict_xpaths='/html/body/div/div/div/div/a'), callback='parse_event', follow=True),]

	def parse_event(self, response):

		item = EventItem()

		item['title'] = response.xpath('//div/h2/text()').extract_first(default='').strip()
		item['description'] = self.format_description(response.xpath('//div[contains(@class, "col-xs-12")]')[1].extract())
		item['eventWebsite'] = response.url

		address_block = response.xpath('//div[@class="row"]/div[contains(@class,"col-lg-12")]/text()')
		for element in address_block:
			if "-" in element.extract() and "-" not in address_block[address_block.index(element)-1].extract():
				street = address_block[address_block.index(element)-2].extract().strip()
				city = address_block[address_block.index(element)-1].extract().strip().split(',')[0]
				state = address_block[address_block.index(element)-1].extract().strip().split(',')[1].strip().split(' ')[0]
				zip = address_block[address_block.index(element)-1].extract().strip().split(',')[1].strip().split(' ')[1]
		item['city'] = city
		item['state'] = state
		item['zip'] = zip
		item['street'] = street

		try:
			item['dateFrom'] = self.date_converter(response.xpath('//div[contains(@class,"col-lg-8")]/span/text()')[1].extract().strip().split('\n')[0])
		except:
			item['dateFrom'] = ''

		try:
			item['startTime'] = self.time_converter(response.xpath('//div[contains(@class,"col-lg-8")]/span/text()')[1].extract().strip().split('\n')[1].strip())
		except:
			item['startTime'] = ''
		item['In_group_id'] = ''
		item['ticketUrl'] = ''
		item['eventImage'] =  "http:" + response.xpath('//div[contains(@class,"col-lg-8")]/div[contains(@class,"col-sm-2")]/img/@src').extract_first(default='')
		item['organization'] = "Barnes & Noble"

		return item

	@staticmethod
	def format_description(raw_description):
		description = ""
		description = remove_tags(raw_description).replace('  ','')
		return description

	@staticmethod
	def date_converter(raw_date):
		raw_date_datetime_object = datetime.strptime(raw_date.replace(',',''), '%A %B %d %Y')
		final_date = raw_date_datetime_object.strftime('%d/%m/%Y')
		return final_date

	@staticmethod
	def time_converter(raw_time):
		raw_time_datetime_object = datetime.strptime(raw_time, '%I:%M %p')
		final_time = raw_time_datetime_object.strftime('%I:%M %p')
		return final_time


