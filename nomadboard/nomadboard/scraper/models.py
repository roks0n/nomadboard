from django.db import models


class Scraper(models.Model):
    """
    Scraper model

    """
    name = models.CharField(max_length=80, unique=True)
    url = models.CharField(max_length=150, unique=True, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Scraper {name}>'.format(name=self.name)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Scraper, self).save(*args, **kwargs)


CATEGORY_PROGRAMMING = 'programming'
CATEGORY_DESIGN = 'design'
CATEGORY_DEVOPS = 'devops'
CATEGORY_MARKETING = 'marketing'
CATEGORIES = (
    (CATEGORY_PROGRAMMING, 'Programming'),
    (CATEGORY_DESIGN, 'Design'),
    (CATEGORY_DEVOPS, 'DevOps'),
    (CATEGORY_MARKETING, 'Marketing'),
)


class Source(models.Model):
    """
    Source model

    """
    scraper = models.ForeignKey(Scraper, related_name='sources', related_query_name='scraper',
                                on_delete=models.CASCADE, null=True, blank=True)
    url = models.CharField(max_length=300, unique=True)
    category = models.CharField(choices=CATEGORIES,
                                default=CATEGORY_PROGRAMMING,
                                blank=True, max_length=11)


    def __str__(self):
        return self.url

    def __repr__(self):
        return '<Source {} from {}>'.format(self.url, self.scraper)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Source, self).save(*args, **kwargs)
