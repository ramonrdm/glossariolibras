from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'glossario.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin', include(admin.site.urls)),
    url(r'^(?P<glossario>[-\w]+)$', 'glossario.views.index', name='glossarios'),
    url(r'^index/equipe', 'glossario.views.equipe'),
    url(r'^index/contato', 'glossario.views.contato'),
    url(r'^index/historia', 'glossario.views.historia'),
    url(r'^(?P<glossario>[-\w]+)/(?P<tipopesq>[\w]+)$', 'glossario.views.pesquisa'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
)+static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
