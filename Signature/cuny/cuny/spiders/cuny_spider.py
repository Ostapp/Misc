import scrapy
from cuny.items import EventItem
from scrapy.spiders import CrawlSpider, Rule
from datetime import datetime

class CunySpider(CrawlSpider):
	name = "events"

	start_urls = ['https://events.cuny.edu/et/lectures/',]

	def parse(self, response):

		events = response.xpath('//div[@class="wpb_wrapper"]/ul/li[contains(@class,"box")]')

		for event in events:

			item = EventItem()

			factor = -1

			try: 
				if event.xpath('div/h4/text()')[1].extract().strip() == 'Tags:':
					factor = 1
					tags = []
					for tag in event.xpath('div/h4/a/text()'):
						tags.append(tag.extract())
					tags = ", ".join(tags)
					item['eventTags'] = tags
				else:
					item['eventTags'] = ''
					factor = -1
			except:
				factor = -1
				item['eventTags'] = ''

			item['title'] = event.xpath('div/h2/a/text()').extract_first(default='')
			item['description'] = event.xpath('div/text()').extract_first(default='')
			item['eventWebsite'] = event.xpath('div/h2/a/@href').extract_first(default='')
			item['organization'] = event.xpath('div/h4/text()').extract_first(default='')

			item['city'] = 'New York'
			item['state'] = 'NY'
			item['zip'] = '10016'
			item['street'] = '365 5th Ave'

			try:
				item['dateFrom'] = self.date_converter(event.xpath('div/h4/text()')[2+factor].extract())
			except:
				item['dateFrom'] = ''

			try:
				item['startTime'] = self.time_converter(event.xpath('div/h4/text()')[3+factor].extract().split(u'\u2014')[0].strip())
			except Exception as e:
				print e
				item['startTime'] = ''
			try:				
				item['endTime'] = self.time_converter(event.xpath('div/h4/text()')[3+factor].extract().split(u'\u2014')[1].strip())
			except:
				item['endTime'] = ''
			item['In_group_id'] = ''
			item['ticketUrl'] = ''
			item['eventImage'] = ''

			yield item

		next_page = response.xpath('//div[@class="pagination"]/a/@href')[-1].extract()

		if next_page:
			 yield response.follow(next_page, callback=self.parse)

	@staticmethod
	def format_description(raw_description):
		description = ""
		description = remove_tags(raw_description).replace('  ','')
		return description

	@staticmethod
	def date_converter(raw_date):
		raw_date_datetime_object = datetime.strptime(raw_date.replace(',',''), '%B %d %Y')
		final_date = raw_date_datetime_object.strftime('%d/%m/%Y')
		return final_date

	@staticmethod
	def time_converter(raw_time):
		raw_time_datetime_object = datetime.strptime(raw_time, '%I:%M %p')
		final_time = raw_time_datetime_object.strftime('%I:%M %p')
		return final_time


