# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import pymongo
from scrapy.item import Item


class MyspiderPipeline(object):
    def process_item(self, item, spider):
        return item


# 汇率转换
class PriceConverterPipeline(object):
    # 英镑兑换人民币汇率
    exchange_rate = 8.5309

    def process_item(self, item, spider):
        # 提取item的price 字段（如￡53.74）
        # 去掉前面英镑符号￡，转换为float 类型，乘以汇率
        price = float(item['price'][1:]) * self.exchange_rate
        # 保留2 位小数，赋值回item的price 字段
        item['price'] = '￥%.2f' % price
        return item


# 过滤重复数据
class DuplicatesPipeline(object):
    def __init__(self):
        self.book_set = set()

    def process_item(self, item, spider):
        name = item['name']
        if name in self.book_set:
            raise DropItem('Duplicate book found :%s' % item)
        self.book_set.add(name)
        return item


# 将数据存储到数据库
class MongoDBPipeline(object):
    DB_URL = 'mongodb://localhost:27017/'
    DB_NAME = 'scrapy_data'

    # 爬虫开始前链接数据库
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.DB_URL)
        self.db = self.client[self.DB_NAME]

    # 爬虫结束后断开数据库链接
    def close_spider(self, spider):
        # 关闭链接
        self.client.close()

    def process_item(self, item, spider):
        # 实现MongoDB数据库的写入操作，使用self.db和spider.name获取一个集合
        collection = self.db[spider.name]
        """
        集合对象的insert_one方法需传入一个字典对象（不能传入Item对象）
        因此在调用前先对item的类型进行判断，如果item是Item对象，就将其转换为字典。
        """
        post = dict(item) if isinstance(item, Item) else item
        collection.insert_one(post)
        return item
