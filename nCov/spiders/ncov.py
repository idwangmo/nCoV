# -*- coding: utf-8 -*-
import json
import logging

import redis
import requests
import scrapy

r = redis.Redis()


class NcovSpider(scrapy.Spider):
    name = 'ncov'
    allowed_domains = ['dxy.cn']
    start_urls = [
        'https://3g.dxy.cn/newh5/view/pneumonia?from=groupmessage&isappinstalled=0'
    ]
    left_str = '<script id="getTimelineService">try { window.getTimelineService'
    right_str = '}catch(e){}</script>'
    seckey = str(r.get('push_key'), encoding="utf-8")
    ncov_id = str(r.get('ncov'), encoding="utf-8")

    def parse(self, response):
        script_body = response.xpath('//*[@id="getTimelineService"]').get()
        body = str(script_body).lstrip(self.left_str).rstrip(self.right_str)
        ncov_body = json.loads(body)[0]

        if str(ncov_body['id']) != self.ncov_id:
            self.push(ncov_body)
            r.set('ncov', str(ncov_body['id']))
        else:
            logging.info("没有新的消息")

    def push(self, body):
        content = (body['summary'] + '\r\n\r\n --- \r\n\r\n ⚠️ 如发现标题编号不连续，请点击下边疫情页确认可能错过的播报。 \r\n\r\n 💊 [消息源:' + body[
            'infoSource'] + '](' + body['sourceUrl'] + ')  💊 [丁香园疫情页](https://3g.dxy.cn/newh5/view/pneumonia) ')

        post_data = {
            'text': body['id'] + '.' + body['title'],
            'desp': content
        }
        url = 'https://sc.ftqq.com/' + self.seckey + '.send'

        log = requests.post(url=url, data=post_data)
        logging.info(str(log.content, encoding="utf-8"))
