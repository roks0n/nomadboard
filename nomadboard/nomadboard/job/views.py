from django.views.generic.base import TemplateView

from nomadboard.nomadboard.job.models import Job


class JobBoard(TemplateView):

    template_name = 'main.jinja'

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
