import scrapy
from nyhistory.items import EventItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime
from w3lib.html import remove_tags
from scrapy.selector import Selector
import re

class NyhistorySpider(CrawlSpider):

	name = "events_details"
	
	custom_settings = {
		'ITEM_PIPELINES': {
			'nyhistory.pipelines.NyhistoryPipelineDetails': 400
		}
	}
	start_urls = ['http://www.nyhistory.org/programs/upcoming-public-programs',]

	rules = [Rule(LinkExtractor(allow='.*?page=.*',restrict_xpaths='//li[@class="pager-next"]'), follow=True),
			Rule(LinkExtractor(restrict_xpaths='//div[@class="view-content"]/div[contains(@class,"views-row")]'), callback='parse_event_details'),
			]

	def parse_event_details(self, response):

		base_url = 'http://www.nyhistory.org'

		item = EventItem()
		item['title'] = response.xpath('//div[@class="views-field-title"]//text()')[2].extract()
		item['eventWebsite'] = response.url

		details_area = response.xpath('//div[@class="body-programs"]')
		details_area_str = " ".join(details_area.extract())
		details_area_str_split = re.split('EVENT DETAILS|LOCATION|PURCHASING TICKETS', details_area_str)
		speakers_names_area = details_area_str_split[1]
		speakersNames = Selector(text=speakers_names_area).xpath('strong').extract()
		try:
			item['speaker1FirstName'] = speakersNames[0].split()[0]
			item['speaker1LastName'] = speakersNames[0].split()[1]
		except:
			item['speaker1FirstName'] = ''
			item['speaker1LastName'] = ''

		description = remove_tags(details_area_str_split[1]).strip()
		item['description'] = description

		try:
			address_line = remove_tags(details_area_str_split[2]).strip()
			item['location'] = address_line.split(',')[0]
			item['city'] = address_line.split(',')[-2].strip()
			item['state'] = address_line.split(',')[-1].split()[0]
			item['zip'] = address_line.split(',')[-1].split()[1]
			item['street'] = address_line.split(',')[1].strip()
		except:
			item['location'] = ''
			item['city'] = ''
			item['state'] = ''
			item['zip'] = ''
			item['street'] = ''

		try:
			item['dateFrom'] = self.date_converter(response.xpath('//span[@class="date-display-single"]/text()').extract_first(default='').rstrip(' - '))
		except:
			try:
				item['dateFrom'] = response.xpath('//span[@class="date-display-single"]/text()').extract()[1].split('|')[0]
			except:
				item['dateFrom'] = ''
		try:
			item['startTime'] = self.time_converter(response.xpath('//span[@class="date-display-start"]/text()')[1].extract())
			# item['endTime'] = self.time_converter(response.xpath('//span[@class="date-display-end"]/text()')[1].extract())
		except:
			try:
				item['startTime'] = self.time_converter(response.xpath('//span[@class="date-display-single"]/text()').extract()[1].split(' | ')[1])
			except:
				item['startTime'] = ''
		item['In_group_id'] = ''
		try:
			item['ticketUrl'] = base_url + response.xpath('//a[contains(@class,"btn-buy-tickets")]/@href').extract_first()
		except:
			item['ticketUrl'] = ''
		item['eventImage'] = response.xpath('//div[@class="views-field-field-speaker-photo-1"]/div/div/img/@src').extract_first(default='')
		item['organization'] = "New York Historical Society"

		yield item

	@staticmethod
	def date_converter(raw_date):
		try:
			raw_date_datetime_object = datetime.strptime(raw_date.replace(',',''), '%a %m/%d/%Y')
			final_date = raw_date_datetime_object.strftime('%d/%m/%Y')
			return final_date
		except:
			raw_date_datetime_object = datetime.strptime(raw_date.replace(',','').replace('th','').strip(), '%a %B %d %Y')
			final_date = raw_date_datetime_object.strftime('%d/%m/%Y')
			return final_date
	@staticmethod
	def time_converter(raw_time):
		raw_time_datetime_object = datetime.strptime(raw_time, '%I:%M %p')
		final_time = raw_time_datetime_object.strftime('%I:%M %p')
		return final_time

