from django.db import models
from django.utils import timezone

from nomadboard.nomadboard.company.models import Company
from nomadboard.nomadboard.scraper.models import Scraper


class Job(models.Model):
    """
    Job model

    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    role = models.CharField(max_length=80)
    visible = models.BooleanField(default=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_published = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=10000)
    tags = models.ManyToManyField('Tag', related_name='tags')
    link = models.CharField(max_length=150)
    via_source = models.ForeignKey(Scraper, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return '{} @ {}'.format(self.role, self.company)

    def __repr__(self):
        return '<Job {title}>'.format(title=self.role)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Job, self).save(*args, **kwargs)


class Tag(models.Model):
    """
    Tag model

    """
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Tag {name}>'.format(name=self.name)
