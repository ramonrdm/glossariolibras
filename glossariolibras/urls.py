from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'glossario.views.index', name='index'),
   
    url(r'^admin/', include(admin.site.urls)),
)+static(settings.STATIC_URL, document_root=settings.STATIC_URL)
