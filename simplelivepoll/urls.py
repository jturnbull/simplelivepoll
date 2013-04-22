from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.views.generic import RedirectView

from . import views


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^favicon.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico')),

    url('^$', views.HomeView.as_view(), name='home'),
    url('^questions/$', views.NextQuestion.as_view(), name='nextquestion'),
    url('^questions/(?P<pk>\w+)/$', views.QuestionView.as_view(), name='question'),
    url('^results/(?P<pk>\w+)/$', views.ResultView.as_view(), name='results'),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
