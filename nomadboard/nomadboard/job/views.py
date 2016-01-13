from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView

from nomadboard.nomadboard.job.models import Job, Tag


class JobBoard(TemplateView):

    template_name = 'main.jinja'
    jobs = None

    def get(self, request, **kwargs):
        jobs = Job.objects.all()
        self.jobs = jobs.order_by('-date_published') if jobs else []
        return super(JobBoard, self).get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(JobBoard, self).get_context_data(**kwargs)

        context.update({
            'jobs': self.jobs
        })

        return context


class JobFilter(TemplateView):

    template_name = 'main.jinja'
    jobs = None

    def get(self, request, **kwargs):
        slug = kwargs.get('tag_slug')
        try:
            jobs = Tag.objects.get(name=slug).jobs.all()
        except Tag.DoesNotExist:
            return HttpResponseRedirect(reverse('home'))
        jobs = Tag.objects.get(name=slug).jobs.all()
        self.jobs = jobs.order_by('-date_published') if jobs else []
        return super(JobFilter, self).get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(JobFilter, self).get_context_data(**kwargs)

        context.update({
            'jobs': self.jobs
        })

        return context
