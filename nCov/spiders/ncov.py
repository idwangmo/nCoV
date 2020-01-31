# -*- coding: utf-8 -*-
import json

import redis
import scrapy

from ..items import NcovItem

r = redis.Redis()


class NcovSpider(scrapy.Spider):
    name = 'ncov'
    allowed_domains = ['dxy.cn']
    start_urls = [
        'https://3g.dxy.cn/newh5/view/pneumonia?from=groupmessage&isappinstalle\
            d=0'
    ]
    left_str = '<script id="getTimelineService">try { window.getTimelineServic\
        e'

    right_str = '}catch(e){}</script>'
    ncov_id = str(r.get('ncov'), encoding="utf-8")

    def parse(self, response):
        script_body = response.xpath('//*[@id="getTimelineService"]').get()
        body = str(script_body).lstrip(self.left_str).rstrip(self.right_str)
        ncov_body = json.loads(body)[0]

        if str(ncov_body['id']) != self.ncov_id:
            r.set('ncov', str(ncov_body['id']))
            yield self.push(ncov_body)
        else:
            self.logger.info("丁香园没有新消息")

    def push(self, body):
        item = NcovItem()
        item['content'] = (
            body['summary'] +
            '\r\n\r\n --- \r\n\r\n ⚠️ 如发现标题编号不连续，请点击下边疫情页确认可能错\
                过的播报。 \r\n\r\n 💊 [消息源:' + body['infoSource'] + '](' +
            body['sourceUrl'] +
            ')  💊 [丁香园疫情页](https://3g.dxy.cn/newh5/view/pneumonia) ')

        item['title'] = str(body['id']) + '.' + body['title'],

        return item
