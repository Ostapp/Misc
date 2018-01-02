from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from nyhistory_spider_details import NyhistorySpiderEventsUrls
from nyhistory_spider_details import NyhistorySpiderEventsDetails

configure_logging()
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
	yield runner.crawl(NyhistorySpiderEventsUrls)
	yield runner.crawl(NyhistorySpiderEventsDetails)
	reactor.stop()

crawl()
reactor.run()