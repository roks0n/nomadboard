# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-09 19:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scraper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
                ('url', models.CharField(blank=True, max_length=150, null=True, unique=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=300, unique=True)),
                ('category', models.CharField(blank=True, choices=[('programming', 'Programming'), ('design', 'Design'), ('devops', 'DevOps'), ('marketing', 'Marketing')], default='programming', max_length=11)),
                ('scraper', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sources', related_query_name='scraper', to='scraper.Scraper')),
            ],
        ),
    ]
