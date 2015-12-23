# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-05 22:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='uploads')),
                ('slug', models.CharField(blank=True, max_length=80, unique=True)),
                ('visible', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]