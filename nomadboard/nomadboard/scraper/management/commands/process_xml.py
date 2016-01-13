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
        parser.add_argument('--source_id',
                            default=None,
                            help=('You must specify an id of the source you want to fetch and'
                                  'update otherwise we will update all sources.'))
        parser.add_argument('--no_db',
                            default=True,
                            help=('Set to False if you want to update the database with new'
                                  'entries, otherwise use True, which will just output the feed.'
                                  'By default it does not update the database.'))

    def handle(self, *args, **options):
        source_id = options['source_id']
        no_db = options['no_db']

        # start BackgroundScheduler and add an interval job that gets ran every 30 minutes
        scheduler = BackgroundScheduler()
        scheduler.start()
        scheduler.add_job(self.job, 'interval', id='scraper', minutes=30,
                          kwargs={'source_id': source_id})

        try:
            # this keeps the thread alive
            while True:
                sleep(1)
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()

    @staticmethod
    def job(source_id):
        """
        A scraper job that scrapes the feed

        """
        if source_id:
            for source in source_id.split(','):
                try:
                    src = Source.objects.get(pk=int(source))
                except Source.DoesNotExist:
                    src = None
                if src:
                    scrape(src)
