# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-13 20:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='tags',
            field=models.ManyToManyField(related_name='jobs', related_query_name='tags', to='job.Tag'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=80, unique=True),
        ),
    ]
