import scrapy
from nyhistory.items import UrlItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

from scrapy.crawler import CrawlerProcess
import re

class NyhistorySpiderEventsUrls(CrawlSpider):

	name = "events_urls_1"

	custom_settings = {
		'ITEM_PIPELINES': {
			'nyhistory.pipelines.NyhistoryPipelineUrls': 400
		}
	}

	start_urls = ['http://www.nyhistory.org/programs/upcoming-public-programs',]

	rules = [Rule(LinkExtractor(allow='.*?page=.*',restrict_xpaths='//li[@class="pager-next"]'), callback='parse_events_listings', follow=True),]

	def parse_events_listings(self, response):

		base_url = 'http://www.nyhistory.org'

		events_details_urls = [base_url+url for url in response.xpath('//div[@class="view-content"]/div[contains(@class,"views-row")]//a/@href').re(r'.*/programs/.*')]

		for url in events_details_urls:
			item = UrlItem()
			item['url'] = url
			yield item