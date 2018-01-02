import scrapy
from nyhistory.items import EventItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime
from w3lib.html import remove_tags
from scrapy.selector import Selector
import re

class NyhistorySpider(CrawlSpider):

	name = "events"

	start_urls = ['http://www.nyhistory.org/programs/upcoming-public-programs',]

	rules = [Rule(LinkExtractor(allow='.*?page=.*',restrict_xpaths='//li[@class="pager-next"]'), callback='parse_events_listings', follow=True),]

	def __init__(self):
		CrawlSpider.__init__(self)
		self.item = EventItem()

	def parse_start_url(self, response):

		return self.parse_events_listings(response)

	def parse_events_listings(self, response):

		base_url = 'http://www.nyhistory.org'

		events = response.xpath('//div[contains(@class,"views-row")]')

		for event in events:

			self.item = EventItem()

			url = base_url + event.xpath('//span[@class="field-content"]/a/@href').extract_first(default='')

			self.item['title'] = event.xpath('//span[@class="field-content"]/a/text()').extract_first(default='')
			self.item['eventWebsite'] = url
			self.item['dateFrom'] = self.date_converter(event.xpath('//span[@class="date-display-single"]/text()')[1].extract().rstrip(' | '))
			self.item['startTime'] = self.time_converter(event.xpath('//span[@class="date-display-start"]/text()').extract_first(default=''))
			self.item['endTime'] = self.time_converter(event.xpath('//span[@class="date-display-end"]/text()').extract_first(default=''))
			speakersNames = event.xpath('div/div[@class="views-field-field-speaker"]/div/div/text()').extract_first(default='').split(', ')

			try:
				self.item['speaker1FirstName'] = speakersNames[0].split()[0]
				self.item['speaker1LastName'] = " ".join(speakersNames[0].split()[1:])
			except:
				self.item['speaker1FirstName'] = ''
				self.item['speaker1LastName'] = ''
			try:
				self.item['speaker2FirstName'] = speakersNames[1].split()[0]
				self.item['speaker2LastName'] = " ".join(speakersNames[1].split()[1:]).strip(' (moderator)')
			except:
				self.item['speaker2FirstName'] = ''
				self.item['speaker2LastName'] = ''
			self.item['eventPriceNonmembers'] = event.xpath('div/div[@class="views-field-field-program-price"]/div/div/text()').extract_first(default='')
			price_members_raw = event.xpath('div/div[@class="views-field-field-program-member-price"]/span/span/text()').extract_first(default='').strip()
			try:
				price_members = re.sub(r'[a-zA-Z]*','',price_members_raw).strip('(').strip(')').strip()
				self.item['eventPriceMembers'] = price_members
			except:
				self.item['eventPriceMembers'] = ''
			try:
				ticketUrl = event.xpath('div/div[@class="views-field-field-buy-tickets-url"]//a/@href').extract_first(default='')
				if ticketUrl:
					self.item['ticketUrl'] = base_url + event.xpath('div/div[@class="views-field-field-buy-tickets-url"]//a/@href').extract_first(default='')
				else:
					self.item['ticketUrl'] = ''
			except:
				self.item['ticketUrl'] = ''
			
			yield scrapy.Request(url,callback = self.parse_event_details)

	def parse_event_details(self, response):

		details_area = response.xpath('//div[@class="body-programs"]')
		details_area_str = " ".join(details_area.extract())
		details_area_str_split = re.split('EVENT DETAILS|LOCATION|PURCHASING TICKETS', details_area_str)
		description = remove_tags(details_area_str_split[1]).strip()
		self.item['description'] = description

		try:
			address_line = remove_tags(details_area_str_split[2]).strip()
			self.item['location'] = address_line.split(',')[0]
		except:
			self.item['location'] = ''

		self.item['city'] = 'New York'
		self.item['state'] = 'NY'
		self.item['zip'] = '10024'
		self.item['street'] = '170 Central Park West'		

		self.item['eventImage'] = response.xpath('//div[@class="views-field-field-speaker-photo-1"]/div/div/img/@src').extract_first(default='')
		self.item['organization'] = "New York Historical Society"

		return self.item

	@staticmethod
	def date_converter(raw_date):
		try:
			raw_date_datetime_object = datetime.strptime(raw_date.replace(',',''), '%a %m/%d/%Y')
			final_date = raw_date_datetime_object.strftime('%d/%m/%Y')
			return final_date
		except:
			try:
				raw_date_datetime_object = datetime.strptime(raw_date.replace(',','').replace('th','').replace('st','').strip(), '%a %B %d %Y')
				final_date = raw_date_datetime_object.strftime('%d/%m/%Y')
			except:
				final_date = ''
			return final_date

	@staticmethod
	def time_converter(raw_time):
		try:
			raw_time_datetime_object = datetime.strptime(raw_time, '%I:%M %p')
			final_time = raw_time_datetime_object.strftime('%I:%M %p')
		except:
			final_time = ''
		return final_time

