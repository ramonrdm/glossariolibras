from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from glossario import views
from django.views.static import serve

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin', admin.site.urls),
    url(r'^equipe', views.equipe, name='equipe'),
    url(r'^contato', views.contato, name='contato'),
    url(r'^historia', views.historia, name='historia'),
    url(r'^temas$', views.temas, name='temas'),
    url(r'^temasjson', views.temasjson, name='temasjson'),
    url(r'^sinal/(\d+)$', views.sinal, name='sinal'),
    url(r'^enviarsinais', views.enviarSinais, name='enviarsinais'),
    url(r'^(?P<glossario>[-\w]+)$', views.glossarioSelecionado, name='glossarios'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)