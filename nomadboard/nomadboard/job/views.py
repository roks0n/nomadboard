from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView

from nomadboard.nomadboard.job.models import Job, Tag
from nomadboard.nomadboard.utils.pagination import pagination as paginator


class JobBoard(TemplateView):

    template_name = 'main.jinja'

    def get(self, request, **kwargs):
        return super(JobBoard, self).get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(JobBoard, self).get_context_data(**kwargs)
        page = self.request.GET.get('page')
        jobs = Job.objects.all().order_by('-date_published')

        paginated_jobs = paginator(jobs, page, 6)
        if paginated_jobs:
            jobs = paginated_jobs

        context.update({
            'jobs': jobs,
        })

        return context


class JobFilter(TemplateView):

    template_name = 'main.jinja'

    def get(self, request, **kwargs):
        return super(JobFilter, self).get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(JobFilter, self).get_context_data(**kwargs)
        page = self.request.GET.get('page')
        slug = kwargs.get('tag_slug')

        try:
            tag = Tag.objects.get(name=slug)
        except Tag.DoesNotExist:
            return HttpResponseRedirect(reverse('home'))

        jobs = Tag.objects.get(name=slug).jobs.order_by('-date_published') if tag else []

        paginated_jobs = paginator(jobs, page, 6)

        if paginated_jobs:
            jobs = paginated_jobs
        context.update({
            'jobs': jobs,
            'tag_slug': slug,
        })

        return context
