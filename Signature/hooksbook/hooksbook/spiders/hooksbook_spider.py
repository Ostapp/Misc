import scrapy
from hooksbook.items import EventItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime
import re

class HooksbookSpider(CrawlSpider):

	name = "events"
	
	start_urls = ['https://hooksbookevents.com/events/',]

	rules = [Rule(LinkExtractor(restrict_xpaths='//li[contains(@class,"tribe-events-nav-right")]'), follow=True),
			Rule(LinkExtractor(restrict_xpaths='//h2[@class="tribe-events-list-event-title"]'), callback='parse_event_details'),
			]

	def parse_event_details(self, response):

		item = EventItem()
		try:
			item['title'] = response.xpath('//h1[@class="tribe-events-single-event-title"]/text()').extract_first(default='')
		except:
			item['title'] = ''
		item['eventWebsite'] = response.url

		try:
			item['description'] = " ".join(response.xpath('//div[@class="wpb_wrapper"]/div[contains(@class,"wpb_content_element")]/div[@class="wpb_wrapper"]/p/text()')[:-3].extract())
		except:
			item['description']	= ''

		try:
			address_line = response.xpath('//dd[@class="tribe-venue"]/a/text()').extract_first(default='')
		except:
			pass

		try:
			item['city'] = address_line.split(',')[0].strip()
		except:
			item['city'] = ''
		try:
			item['state'] = address_line.split(',')[1].strip()
		except:
			item['state'] = ''

		item['zip'] = ''
		item['street'] = ''

		item['dateFrom'] = self.date_converter(response.xpath('//abbr[contains(@class,"tribe-events-start-datetime")]/@title').extract_first(default=''))
		item['In_group_id'] = ''
		item['eventImage'] = response.xpath('//div[contains(@class,"vc_single_image-wrapper")]/img/@src').extract_first(default='')
		item['organization'] = "Hooks Book Events"
		item['eventType'] = response.xpath('//dd[@class="tribe-events-event-categories"]/a/text()').extract_first(default='')

		yield item

	@staticmethod
	def date_converter(raw_date):
		raw_date_datetime_object = datetime.strptime(raw_date, '%Y-%m-%d')
		final_date = raw_date_datetime_object.strftime('%d/%m/%Y')
		return final_date

