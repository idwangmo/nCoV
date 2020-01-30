# -*- coding: utf-8 -*-
import json
import re

import redis
import scrapy

from ..util import push_serverchain

r = redis.Redis()


class A2019ncovSpider(scrapy.Spider):
    name = '2019ncov'
    allowed_domains = ['47.75.131.65:9918']
    start_urls = ['http://47.75.131.65:9918/api']
    seckey = str(r.get("push_key"), encoding="utf-8")
    ncov_status = str(r.get("2019ncov"), encoding="utf-8")

    def parse(self, response):
        json_body = json.loads(str(response.body, encoding="utf-8"))
        items = json_body['items']
        ncov_news = items[0]

        if ncov_news['guid'] != self.ncov_status:
            self.push(ncov_news)
            r.set('2019ncov', ncov_news['guid'])

    def push(self, ncov):
        title = re.search(r'(?<=【)[^】]+',
                          ncov['title']).group(0).replace('#', '')
        content = (str(ncov['contentSnippet']).replace('#', '') +
                   '\r\n\r\n --- \r\n\r\n [消息源](' + ncov['link'] + ')')
        response = push_serverchain(title, content, self.seckey)
        self.logger.info(response)
