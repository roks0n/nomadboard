from django.core.management.base import BaseCommand, CommandError

from nomadboard.nomadboard.scraper.models import Source

from nomadboard.nomadboard.scraper.scrapers.weworkremotely import scrape


class Command(BaseCommand):
    help = 'Fetch feed(s) and update nomadboard.'

    def add_arguments(self, parser):
        parser.add_argument('--source_id',
                            default=None,
                            help=('You must specify an id of the source you want to fetch and update'
                                  'otherwise we will update all sources.'))
        parser.add_argument('--no_db',
                            default=True,
                            help=('Set to False if you want to update the database with new entries,'
                                  'otherwise use True, which will just output the feed. By default'
                                  'it does not update the database.'))

    def handle(self, *args, **options):
        source_id = options['source_id']
        no_db = options['no_db']

        if source_id:
            try:
                src = Source.objects.get(pk=int(source_id))
            except Source.DoesNotExist:
                src = None

            if src:
                scrape(src)

        else:
            # something else
            pass

        # raise CommandError('Source does not exist')
