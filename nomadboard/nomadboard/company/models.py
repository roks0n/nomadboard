from django.db import models
from django.utils import timezone


class Company(models.Model):
    """
    Company model

    """
    name = models.CharField(max_length=80, unique=True)
    logo = models.ImageField(upload_to='uploads', blank=True, null=True)
    slug = models.CharField(max_length=80, unique=True, blank=True)
    visible = models.BooleanField(default=True)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Company {name}>'.format(name=self.name)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Company, self).save(*args, **kwargs)
