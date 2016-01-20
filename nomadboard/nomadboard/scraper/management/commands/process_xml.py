from time import sleep

from apscheduler.schedulers.background import BackgroundScheduler

from django.core.management.base import BaseCommand

from nomadboard.nomadboard.scraper.models import Source
from nomadboard.nomadboard.scraper.scrapers.weworkremotely import scrape


class Command(BaseCommand):
    """
    Django admin command that runs a scheduler for scrapers

    """
    help = 'Fetch feed(s) and update nomadboard.'

    def add_arguments(self, parser):
        parser.add_argument('--source_ids',
                            default=None,
                            help=('You must specify an id of the source you want to fetch and'
                                  'update otherwise we will update all sources.'))

    def handle(self, *args, **options):
        source_ids = options['source_ids']

        # start BackgroundScheduler and add an interval job that gets ran every 30 minutes
        scheduler = BackgroundScheduler()
        scheduler.start()
        scheduler.add_job(self.job, 'interval', id='scraper', minutes=30,
                          kwargs={'source_ids': source_ids})

        try:
            # this keeps the thread alive
            while True:
                sleep(1)
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()

    @staticmethod
    def job(source_ids):
        """
        A scraper job that scrapes the feed

        """
        filters = {}
        if source_ids:
            sources = source_ids.split(',')
            filters['pk__in'] = sources

        for source in Source.objects.filter(**filters):
            scrape(source)
