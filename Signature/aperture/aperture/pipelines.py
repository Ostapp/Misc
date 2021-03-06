# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json

class AperturePipeline(object):
	def open_spider(self, spider):
		self.file = open(os.path.dirname(__file__) + '/../events.json','w')
		self.file.write("[")


	def close_spider(self, spider):
		self.file.write("]")
		self.file.close()

	def process_item(self, item, spider):
		line = json.dumps(
			dict(item),
			sort_keys=True,
			indent=4,
			separators=(',', ': ')
		) + ",\n"

		self.file.write(line)
		return item
