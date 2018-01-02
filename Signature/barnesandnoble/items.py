# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class EventItem(scrapy.Item):
	organization = scrapy.Field()
	title = scrapy.Field()
	description = scrapy.Field()
	eventWebsite = scrapy.Field()
	street = scrapy.Field()
	city = scrapy.Field()
	state = scrapy.Field()
	zip = scrapy.Field()
	dateFrom = scrapy.Field()
	startTime = scrapy.Field()
	In_group_id = scrapy.Field()
	ticketUrl = scrapy.Field()
	eventImage = scrapy.Field()


