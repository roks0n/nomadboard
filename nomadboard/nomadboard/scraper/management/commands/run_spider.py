# -*- coding: utf-8 -*-
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

        if not scraper_slug:
            raise ValueError

        scraper = Scraper.objects.get(slug=scraper_slug)
        spider_cls = api.get_spider(scraper.slug)
        spider = spider_cls()
        spider.start()
