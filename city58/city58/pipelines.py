# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from .items import *
from scrapy.item import Item
import pymongo


# class City58Pipeline(object):
#
#     def open_spider(self, spider):
#         self.file = open('58_chuzu.txt', 'w', encoding='utf-8')
#         print("打开文件了")
#
#     def process_item(self, item, spider):
#         line = '{}\n'.format(json.dumps(dict(item), ensure_ascii=False))
#         self.file.write(line)
#         return item
#
#     def close_spider(self, spider):
#         self.file.close()
#         print("关闭文件了")


class MongoDBPipeline(object):
    DB_URI = 'mongodb://localhost:27017'
    DB_NAME = '58zufang_data'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.DB_URI)
        self.db = self.client[self.DB_NAME]

    def process_item(self, item, spider):
        collection = self.db[spider.name]
        post = dict(item) if isinstance(item, Item) else item
        collection.insert_one(post)

    def close_spider(self, spider):
        self.client.close()
