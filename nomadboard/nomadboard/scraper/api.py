# -*- coding: utf-8 -*-
import inspect
import os
from datetime import datetime
from importlib import import_module
from pkgutil import iter_modules
from urllib.parse import urlparse

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.utils.text import slugify

from nomadboard.nomadboard.company.models import Company
from nomadboard.nomadboard.job.models import Job, Tag
from nomadboard.nomadboard.job.utils import extract_and_normalize_tags
from nomadboard.nomadboard.scraper.models import Scraper
from nomadboard.nomadboard.scraper.scrapers.base import Spider

import requests


SCRAPERS_MODULE = 'nomadboard.nomadboard.scraper.scrapers'


def _download_and_save_logo(company, url):
    """
    Download and save logo to the company

    :param company: Company object
    :param url: logo url
    :returns: None

    """

    file_name = '{}.{}'.format(datetime.now().strftime('%Y%m%d'),
                               os.path.basename(urlparse(url).path))
    response = requests.get(url)

    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(response.content)
    img_temp.flush()
    company.logo.save(file_name, File(img_temp), save=True)


def get_scraper(name, slug):
    """
    Gets or creates a Scraper object and returns it.

    :param name: Spider/Scraper name
    :param slug: slug
    :returns: Scraper object

    """

    scraper, created_company = Scraper.objects.get_or_create(
        slug=slug,
        defaults={
            'name': name,
        }
    )

    return scraper


def _get_company(name, logo_url):
    """
    Updates or creates a Company and returns it.

    :param name: company name
    :param logo_url: logo url
    :returns: Company object

    """

    company_name = name.strip()
    company, created_company = Company.objects.get_or_create(
        slug=slugify(company_name),
        name=company_name,
    )

    # TODO: What happens when the logo changes for the company?
    if logo_url and not company.logo:
        _download_and_save_logo(company, logo_url)

    return company


def _create_job(scraper, company, job_data):
    """
    Creates or updates a Job and it's Tags

    :param scraper: Scraper object
    :param company: Company object
    :param job_data: dictionary containing

    """

    try:
        job, created_job = Job.objects.update_or_create(
            company=company,
            link=job_data['link'],
            via_source=scraper,
            defaults={
                'role': job_data['role'],
                'date_published': job_data['date_published'],
                'description': job_data['description'],
            }
        )
    except:
        # TODO: add logging here to see what sort of errors we get
        return None

    if created_job:
        tag, _ = Tag.objects.get_or_create(name=job_data['source_category'])
        if not job.tags.filter(name=tag).exists():
            job.tags.add(tag)

    tags = []
    extracted_tags = extract_and_normalize_tags(job.role)
    for tag_name in extracted_tags:
        tag, _ = Tag.objects.get_or_create(name=tag_name)
        tags.append(tag)

    job.tags.add(*tags)
    job.save()
    return job


def _walk_modules(path):
    """
    Loads a module and all its submodules from the given module path

    :param path: module path
    :returns: list of modules

    """

    mods = []
    mod = import_module(path)
    mods.append(mod)
    if hasattr(mod, '__path__'):
        for _, subpath, ispkg in iter_modules(mod.__path__):
            fullpath = path + '.' + subpath
            if not ispkg:
                submod = import_module(fullpath)
                mods.append(submod)
    return mods


def iter_spider_classes():
    """
    Return an iterator over all spider classes

    """

    for module in _walk_modules(SCRAPERS_MODULE):
        for obj in vars(module).values():
            is_spider_class = bool(
                inspect.isclass(obj) and
                issubclass(obj, Spider) and
                obj.__module__ == module.__name__ and
                obj.slug is not None
            )
            if is_spider_class:
                yield obj


def get_spider(scraper_slug):
    """
    Return spider object

    :param scraper_slug: Scraper object slug

    """

    for spider_cls in iter_spider_classes():
        if spider_cls.slug == scraper_slug:
            return spider_cls


def process_job_data(scraper_slug, job_data):
    scraper = Scraper.objects.get(slug=scraper_slug)

    company = _get_company(job_data['company'], job_data['logo'])

    job = _create_job(scraper, company, job_data)

    return job
