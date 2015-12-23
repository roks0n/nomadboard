from django.contrib import admin

from nomadboard.nomadboard.job.models import Job, Tag


class JobAdmin(admin.ModelAdmin):
     model = Job
     filter_horizontal = ('tags',)


admin.site.register(Job, JobAdmin)
admin.site.register(Tag)
