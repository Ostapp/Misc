import scrapy
from aperture.items import EventItem
from scrapy.spiders import CrawlSpider
from datetime import datetime
from w3lib.html import remove_tags

class ApertureSpider(scrapy.Spider):
	# year is hardcoded, line 64
	name = "events"

	def start_requests(self):
		urls = ['https://aperture.org/events/',]

		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):

		events = response.xpath('//ul[@class="day-events"]/li')
		valid_events_urls = []

		for event in events:
			if event.xpath('div/text()').extract_first() == "Talk" or event.xpath('div/text()').extract_first() == "Special Event":
				valid_events_urls.append(event.xpath('a/@href').extract_first())

		for url in valid_events_urls:
			yield scrapy.Request(url, callback=self.parse_event)


	def parse_event(self, response):

		item = EventItem()
		item['title'] = response.xpath('//p[@class="event-title"]/text()').extract_first(default='').strip()
		item['description'] = " ".join([p.extract() for p in response.xpath('//div[@class="event-description"]//p/text()')])
		item['eventWebsite'] = response.url

		try:
			item['speaker1FirstName'] = remove_tags(response.xpath('//div[@class="event-description"]//p/strong').extract()[0]).split(' ')[0]
		except:
			item['speaker1FirstName'] = ''
		try:
			item['speaker1LastName'] = remove_tags(response.xpath('//div[@class="event-description"]//p/strong').extract()[0]).split(' ')[1]
		except:
			item['speaker1LastName'] = ''
		try:
			item['speaker2FirstName'] = remove_tags(response.xpath('//div[@class="event-description"]//p/strong').extract()[1]).split(' ')[0]
		except:
			item['speaker2FirstName'] = ''
		try:
			item['speaker2LastName'] = remove_tags(response.xpath('//div[@class="event-description"]//p/strong').extract()[1]).split(' ')[1]
		except:
			item['speaker2LastName'] = ''
			
		address_block = response.xpath('//div[@class="event-information"]/p[@class="event-location"]')
		item['location'] = address_block.xpath('span/text()').extract_first(default='')
		item['city'] = address_block.xpath('span/text()')[2].extract().split(',')[0].strip()
		item['state'] = address_block.xpath('span/text()')[2].extract().split(',')[1].strip()
		item['zip'] = ''
		item['street'] = address_block.xpath('span/text()')[1].extract()

		try:
			item['dateFrom'] = self.date_converter(response.xpath('//p[@class="event-date"]/text()').extract_first(default='').strip())
		except:
			item['dateFrom'] = ''

		time = response.xpath('//p[@class="event-time"]/text()').extract_first(default='').strip()

		if '-' in time:
			item['startTime'] = self.time_converter(time.split(' - ')[0])
			item['endTime'] = self.time_converter(time.split(' - ')[1])
		else:
			item['startTime'] = self.time_converter(time)
		item['In_group_id'] = ''
		item['ticketUrl'] = ''
		item['eventImage'] =  response.xpath('//div[@class="event-images"]/img/@src').extract_first(default='')
		item['organization'] = "Aperture"

		yield item

	@staticmethod
	def date_converter(raw_date):
		raw_date_datetime_object = datetime.strptime(raw_date.replace(',',''), '%A %B %d')
		final_date = raw_date_datetime_object.strftime('%d/%m/2017')
		return final_date

	@staticmethod
	def time_converter(raw_time):
		raw_time_datetime_object = datetime.strptime(raw_time, '%I:%M %p')
		final_time = raw_time_datetime_object.strftime('%I:%M %p')
		return final_time

