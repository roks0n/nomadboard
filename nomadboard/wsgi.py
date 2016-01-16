"""
WSGI config for nomadboard project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.utils import autoreload

import uwsgi

from uwsgidecorators import timer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nomadboard.settings')

application = get_wsgi_application()


@timer(3)
def change_code_gracefull_reload(sig):
    if autoreload.code_changed():
        uwsgi.reload()
