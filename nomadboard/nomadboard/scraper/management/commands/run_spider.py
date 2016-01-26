# -*- coding: utf-8 -*-
from time import sleep

from apscheduler.schedulers.background import BackgroundScheduler

from django.core.management.base import BaseCommand

from nomadboard.nomadboard.scraper import api
from nomadboard.nomadboard.scraper.models import Scraper


class Command(BaseCommand):
    """
    Django admin command that runs a scheduler for scrapers

    """
    help = 'Fetch feed(s) and update nomadboard.'

    def add_arguments(self, parser):
        parser.add_argument('--scraper_slug',
                            default=None,
                            help=('Specify a slug of the Scraper you want to fetch data from'))

    def handle(self, *args, **options):
        scraper_slug = options['scraper_slug']

        # start BackgroundScheduler and add an interval job that gets ran every 30 minutes
        scheduler = BackgroundScheduler()
        scheduler.start()
        scheduler.add_job(self.job, 'interval', id='scraper', minutes=30,
                          kwargs={'scraper_slug': scraper_slug})

        try:
            # this keeps the thread alive
            while True:
                sleep(1)
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()

    @staticmethod
    def job(scraper_slug):
        """
        A scraper job that scrapes the feed

        """

        if not scraper_slug:
            raise ValueError

        scraper = Scraper.objects.get(slug=scraper_slug)
        spider_cls = api.get_spider(scraper.slug)
        spider = spider_cls()
        spider.start()
