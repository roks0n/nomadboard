# -*- coding: utf-8 -*-
from nomadboard.nomadboard.scraper import api

import requests


class Spider(object):
    name = None
    slug = None

    urls = []

    def start(self):
        for url in self.urls:
            response = requests.get(url)
            for job_data in self.parse(response):
                api.process_job_data(self.slug, job_data)

    def parse(self, response):
        raise NotImplemented
