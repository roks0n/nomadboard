# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView

from nomadboard.nomadboard.job.models import Job, Tag
from nomadboard.nomadboard.utils import pagination

JOBS_PER_PAGE = 6


class JobBoard(TemplateView):

    template_name = 'main.jinja'

    def get_context_data(self, **kwargs):
        context = super(JobBoard, self).get_context_data(**kwargs)

        page = self.request.GET.get('page')
        jobs = Job.objects.all().order_by('-date_published')

        paginated_jobs = pagination.get_paginator(jobs, page, JOBS_PER_PAGE)
        if paginated_jobs:
            jobs = paginated_jobs

        context.update({
            'jobs': jobs,
        })

        return context


class JobFilter(TemplateView):

    template_name = 'main.jinja'

    def get_context_data(self, **kwargs):
        context = super(JobFilter, self).get_context_data(**kwargs)

        page = self.request.GET.get('page')
        tag_name = kwargs.get('tag_slug')

        try:
            tag = Tag.objects.get(name=tag_name)
        except Tag.DoesNotExist:
            return HttpResponseRedirect(reverse('home'))

        jobs = tag.jobs.order_by('-date_published')

        paginated_jobs = pagination.get_paginator(jobs, page, JOBS_PER_PAGE)
        if paginated_jobs:
            jobs = paginated_jobs

        context.update({
            'jobs': jobs,
            'tag_slug': tag_name,
        })
        return context
