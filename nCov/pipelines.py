# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
import logging


class NcovPipeline(object):
    def __init__(self, server_chain_key):
        self.server_chain_key = server_chain_key

    @classmethod
    def from_crawler(cls, crawler):
        return cls(server_chain_key=crawler.settings.get('SERVER_CHAIN_KEY'))

    def process_item(self, item, spider):
        post_data = {'text': item['title'], 'desp': item['content']}
        url = f'https://sc.ftqq.com/{self.server_chain_key}.send'

        response = requests.post(url=url, data=post_data)
        logging.info(str(response.content, encoding="utf-8"))
        return item
