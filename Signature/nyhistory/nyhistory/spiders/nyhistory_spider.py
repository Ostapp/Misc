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

	rules = [Rule(LinkExtractor(allow='.*?page=.*',restrict_xpaths='//li[@class="pager-next"]'), follow=True),
			Rule(LinkExtractor(restrict_xpaths='//div[@class="view-content"]/div[contains(@class,"views-row")]'), callback='parse_event_details'),
			]

	def parse_event_details(self, response):

		base_url = 'http://www.nyhistory.org'

		item = EventItem()
		try:
			item['title'] = response.xpath('//div[@class="views-field-title"]//text()')[2].extract()
		except:
			item['title'] = ''
		item['eventWebsite'] = response.url
		try:
			details_area = response.xpath('//div[@class="body-programs"]')
			details_area_str = " ".join(details_area.extract())
			details_area_str_split = re.split('EVENT DETAILS|LOCATION|PURCHASING TICKETS', details_area_str)
			speakers_names_area = details_area_str_split[1]
			speakersNames = Selector(text=speakers_names_area).css('strong::text').extract()
		except Exception as e:
			print (e)
			pass
		try:
			item['speaker1FirstName'] = speakersNames[0].split()[0]
			item['speaker1LastName'] = speakersNames[0].split()[1]
		except:
			item['speaker1FirstName'] = ''
			item['speaker1LastName'] = ''

		try:
			item['speaker2FirstName'] = speakersNames[1].split()[0]
			item['speaker2LastName'] = speakersNames[1].split()[1]
		except Exception as e:
			item['speaker2FirstName'] = ''
			item['speaker2LastName'] = ''

		description = remove_tags(details_area_str_split[1]).strip()
		item['description'] = description

		try:
			address_line = remove_tags(details_area_str_split[2]).strip()
			item['location'] = address_line.split(',')[0]
		except:
			item['location'] = ''

		item['city'] = 'New York'
		item['state'] = 'NY'
		item['zip'] = '10024'
		item['street'] = '170 Central Park West'

		try:
			item['dateFrom'] = self.date_converter(response.xpath('//span[@class="date-display-single"]/text()').extract_first(default='').rstrip(' - '))
		except:
			try:
				item['dateFrom'] = self.date_converter(response.xpath('//span[@class="date-display-single"]/text()').extract()[1].split('|')[0])
			except:
				item['dateFrom'] = ''
		try:
			item['startTime'] = self.time_converter(response.xpath('//span[@class="date-display-start"]/text()')[1].extract())
		except:
			try:
				item['startTime'] = self.time_converter(response.xpath('//span[@class="date-display-single"]/text()').extract()[1].split(' | ')[1])
			except:
				item['startTime'] = ''
		try:
			item['endTime'] = self.time_converter(response.xpath('//span[@class="date-display-start"]/text()')[1].extract())
		except:
			item['endTime'] = ''
		item['In_group_id'] = ''
		item['ticketUrl'] = base_url + response.xpath('//a[contains(@class,"btn-buy-tickets")]/@href').extract_first(default='')
		item['eventImage'] = response.xpath('//div[@class="views-field-field-speaker-photo-1"]/div/div/img/@src').extract_first(default='')
		item['eventPriceNonmembers'] = response.xpath('//div[@class="views-field-field-program-price"]/div/div/text()').extract_first(default='')
		try:
			price_members_raw = response.xpath('//div[@class="views-field-field-program-member-price"]/div/div/text()').extract_first()
			price_members = re.sub(r'[a-zA-Z()]*','',price_members_raw).strip()
			item['eventPriceMembers'] = price_members
		except:
			item['eventPriceMembers'] = ''
		item['organization'] = "New York Historical Society"

		yield item

	@staticmethod
	def date_converter(raw_date):
		try:
			raw_date_datetime_object = datetime.strptime(raw_date.replace(',',''), '%a %m/%d/%Y')
			final_date = raw_date_datetime_object.strftime('%d/%m/%Y')
			return final_date
		except:
			RE_D = re.compile('\d')
			raw_date_list = raw_date.split()
			for raw_string in raw_date_list:
				if RE_D.search(raw_string):
					string = re.sub(r'[^0-9]','', raw_string)
					raw_date_list[raw_date_list.index(raw_string)] = string
			raw_date = " ".join(raw_date_list)
			raw_date_datetime_object = datetime.strptime(raw_date.replace(',','').strip(), '%a %B %d %Y')
			final_date = raw_date_datetime_object.strftime('%d/%m/%Y')
			return final_date
	@staticmethod
	def time_converter(raw_time):
		raw_time_datetime_object = datetime.strptime(raw_time, '%I:%M %p')
		final_time = raw_time_datetime_object.strftime('%I:%M %p')
		return final_time

