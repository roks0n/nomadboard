# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from nomadboard.nomadboard.scraper import api


class Command(BaseCommand):
    """
    Django admin command that sync spiders with the database

    """
    help = 'Sync spiders with the database.'

    def handle(self, *args, **options):

        for spider_cls in api.iter_spider_classes():
            api.get_scraper(spider_cls.name, spider_cls.slug)
