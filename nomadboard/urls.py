"""nomadboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views

from nomadboard.nomadboard.job.views import JobBoard, JobFilter

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', JobBoard.as_view(), name='home'),

    url(r'^job/$', JobFilter.as_view()),
    url(r'^remote-(?P<tag_slug>[\w-]+)-jobs$', JobFilter.as_view(), name='tag'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        url(r'^400/$', default_views.bad_request,
            kwargs={'exception': Exception("Bad Request!")}),
        url(r'^403/$', default_views.permission_denied,
            kwargs={'exception': Exception("Permissin Denied")}),
        url(r'^404/$', default_views.page_not_found,
            kwargs={'exception': Exception("Page not Found")}),
        url(r'^500/$', default_views.server_error),
    ]
