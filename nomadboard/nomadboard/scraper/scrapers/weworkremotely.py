# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from datetime import datetime

from django.utils.html import strip_tags

from nomadboard.nomadboard.scraper import constants
from nomadboard.nomadboard.scraper.scrapers.base import Spider


class WeWorkRemotely(Spider):

    name = 'We Work Remotely'
    slug = 'we-work-remotely'

    urls = [
        'https://weworkremotely.com/categories/6-devops-sysadmin/jobs.rss',
        'https://weworkremotely.com/categories/9-marketing/jobs.rss',
        'https://weworkremotely.com/categories/1-design/jobs.rss',
        'https://weworkremotely.com/categories/2-programming/jobs.rss',
        'https://weworkremotely.com/categories/7-customer-support/jobs.rss',
        'https://weworkremotely.com/categories/3-business-exec-management/jobs.rss',
        'https://weworkremotely.com/categories/5-copywriting/jobs.rss',
    ]

    def _get_category(self, url):
        """
        Find the right category to put the jobs under

        """

        if '6-devops-sysadmin' in url:
            return constants.CATEGORY_DEVOPS
        elif '9-marketing' in url:
            return constants.CATEGORY_MARKETING
        elif '1-design' in url:
            return constants.CATEGORY_DESIGN
        elif '2-programming' in url:
            return constants.CATEGORY_PROGRAMMING
        elif '7-customer-support' in url:
            return constants.CATEGORY_CS
        elif '3-business-exec-management' in url:
            return constants.CATEGORY_EXEC
        elif '5-copywriting' in url:
            return constants.CATEGORY_COPYWRITING

        raise ValueError("Can't find a valid category")

    def parse(self, response):
        root = ET.fromstring(response.content)
        items = root.find('channel').findall('item')
        for item in items:
            logo = None
            if item.find('{http://search.yahoo.com/mrss}content') is not None:
                logo = item.find('{http://search.yahoo.com/mrss}content').attrib['url']

            job_data = {
                'company': item.find('title').text.split(':', 1)[0],
                'role': item.find('title').text.split(':', 1)[1],
                'description': strip_tags(item.find('description').text),
                'link': item.find('link').text,
                'source_category': self._get_category(response.url),
                'date_published': datetime.strptime(
                    item.find('pubDate').text, '%a, %d %b %Y %H:%M:%S %z'),
                'logo': logo
            }

            yield job_data
