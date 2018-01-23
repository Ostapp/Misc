import scrapy
from faccwdc.items import EventItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime
import re

class FaccwdcSpider(CrawlSpider):

	name = "events"
	
	start_urls = ['http://www.faccwdc.org/facc-events/calendar-of-events.html',]

	rules = [
			Rule(LinkExtractor(restrict_xpaths='//table/tr/td/ul/li/a'), callback='parse_event_details'),
			]

	def parse_start_url(self, response):

		yield self.parse_event_details(response)

	def parse_event_details(self, response):

		item = EventItem()
		
		item['title'] = response.xpath('//div[@class="tx-oblady-agenda"]/h1/text()').extract_first(default='')

		item['eventWebsite'] = response.url

		try:
			description_area = " ".join(response.xpath('//div[@class="tx-oblady-agenda"]/p//text()')[3:].extract()).strip()
			description_area_split = re.split('Where|When', description_area)
		except:
			pass
		try:
			address = description_area_split[1].strip().lstrip(': ')
		except:
			pass

		raw_date_and_time = description_area_split[2].split('\r')[0].lstrip(': ')

		try:
			raw_date = self.date_time_prepare(raw_date_and_time)[0]
			raw_start_time = self.date_time_prepare(raw_date_and_time)[1]
			raw_end_time = self.date_time_prepare(raw_date_and_time)[2]
		except:
			raw_date = self.date_time_prepare(address)[0]
			raw_start_time =self.date_time_prepare(address)[1]
			raw_end_time = self.date_time_prepare(address)[2]
			address = raw_date_and_time

		description = description_area_split[0]

		try:
			item['description'] = description
		except:
			item['description'] = ''

		item['city'] = ''
		item['state'] = ''
		item['location'] = address


		item['dateFrom'] = self.date_converter(raw_date)
		item['startTime'] = self.time_converter(raw_start_time)
		item['endTime'] = self.time_converter(raw_end_time)
		item['In_group_id'] = ''
		item['eventImage'] = 'http://http://www.faccwdc.org' + response.xpath('//div[@class="tx-oblady-agenda"]/p/img/@src').extract_first(default='')
		item['organization'] = "FACC"
		item['ticketUrl'] = response.xpath('//a/@href').re('.*event/register.*')
		

		yield item

	@staticmethod
	def date_time_prepare(raw_date_and_time):
	
		raw_date = raw_date_and_time.split(', from ')[0]

		try:
			raw_time = raw_date_and_time.split(', from ')[1].rstrip('. ')
		except:
			raw_time = re.findall(r'\dpm|am',raw_date_and_time)[0]
			raw_date = raw_date_and_time.split(' at ')[0]
			raw_start_time = raw_time
			raw_end_time = ''
			return raw_date, raw_start_time, raw_end_time

		raw_start_time = raw_time.split(' to ')[0]

		if 'p' in raw_start_time and 'pm' not in raw_start_time:
			raw_start_time = raw_start_time.replace('p','pm')
		raw_end_time = raw_time.split(' to ')[1]
		if 'p' in raw_end_time and 'pm' not in raw_end_time:
			raw_end_time = raw_end_time.replace('p','pm')

		return raw_date, raw_start_time, raw_end_time

	@staticmethod
	def date_converter(raw_date):
		try:
			raw_date_datetime_object = datetime.strptime(raw_date, '%a, %b %d, %Y')
			final_date = raw_date_datetime_object.strftime('%d/%m/%Y')
			return final_date
		except:
			try:
				raw_date_datetime_object = datetime.strptime(raw_date, '%A, %b %d, %Y')
				final_date = raw_date_datetime_object.strftime('%d/%m/%Y')
			except:
				try:
					raw_date_datetime_object = datetime.strptime(raw_date, '%b %d, %Y')
					final_date = raw_date_datetime_object.strftime('%d/%m/%Y')
				except:
					try:
						raw_date_datetime_object = datetime.strptime(raw_date, '%a, %b %d. %Y')
						final_date = raw_date_datetime_object.strftime('%d/%m/%Y')		
					except:
						raw_date_datetime_object = datetime.strptime(raw_date, '%a, %b %d')
						final_date = raw_date_datetime_object.strftime('%d/%m/2018')											
		return final_date
	
	@staticmethod
	def time_converter(raw_time):
		if raw_time != '':

			try:
				raw_time_datetime_object = datetime.strptime(raw_time, '%I%p')
				final_time = raw_time_datetime_object.strftime('%I:00 %p')
			except:
				raw_time_datetime_object = datetime.strptime(raw_time, '%I:%M%p')
				final_time = raw_time_datetime_object.strftime('%I:00 %p')
		else:
			final_time = ''
		return final_time
