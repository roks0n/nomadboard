
import os
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.parse import urlparse

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.utils.html import strip_tags
from django.utils.text import slugify

from nomadboard.nomadboard.company.models import Company
from nomadboard.nomadboard.job.models import Job, Tag
from nomadboard.nomadboard.job.utils import extract_and_normalize_tags

import requests


def scrape(source):
    response = requests.get(source.url)
    root = ET.fromstring(response.content)

    jobs = []
    items = root.find('channel').findall('item')
    for item in items:
        job_dict = {
            'company': item.find('title').text.split(':', 1)[0],
            'role': item.find('title').text.split(':', 1)[1],
            'description': strip_tags(item.find('description').text),
            'date_published': datetime.strptime(item.find('pubDate').text,
                                                '%a, %d %b %Y %H:%M:%S %z'),
            'link': item.find('link').text,
            'via_source': source.scraper,
            'source_category': source.category
        }

        if item.find('{http://search.yahoo.com/mrss}content') is not None:
            job_dict['logo'] = item.find('{http://search.yahoo.com/mrss}content')
        else:
            job_dict['logo'] = None

        scraped_job(job_dict)
        jobs.append(job_dict)

    return jobs


def scraped_job(job_dict):
    company_name = job_dict['company'].strip()
    company, created_company = Company.objects.get_or_create(
        slug=slugify(company_name),
        name=company_name,
    )

    if created_company:
        if job_dict['logo'] is not None:
            download_and_save_image(company, job_dict['logo'])

    source_category = job_dict['source_category']
    job_dict.pop('source_category')
    job_dict.pop('logo')
    job_dict.update({'company': company})
    job, created_job = Job.objects.update_or_create(**job_dict)
    if created_job:
        tag, _ = Tag.objects.get_or_create(name=source_category)
        if not job.tags.filter(name=tag).exists():
            job.tags.add(tag)
            job.save()

    tags = []
    extracted_tags = extract_and_normalize_tags(job.role)
    for t in extracted_tags:
        t, _ = Tag.objects.get_or_create(name=t)
        tags.append(t)

    job.tags.add(*tags)
    job.save()


def download_and_save_image(company, logo):
    file_name = '{}.{}'.format(datetime.now().strftime('%Y%m%d'),
                               os.path.basename(urlparse(logo.get('url', None)).path))
    response = requests.get(logo.get('url', None))
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(response.content)
    img_temp.flush()
    company.logo.save(file_name, File(img_temp), save=True)
