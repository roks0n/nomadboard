from django.contrib import admin

from nomadboard.nomadboard.scraper.models import Scraper, Source


admin.site.register(Scraper)
admin.site.register(Source)
