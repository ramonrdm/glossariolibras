
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from glossario import views
from django.views.static import serve
from django.urls import path




from django.conf.urls import url, include


urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('logout/', views.sair, name='logout'),
    path('equipe', views.equipe, name='equipe'),
    path('contato', views.contato, name='contato'),
    path('historia', views.historia, name='historia'),
    path('registration', views.registration, name='registration'),
    path('temas', views.temas, name='temas'),
    path('temasjson', views.temasjson, name='temasjson'),
    path('sinal/<int:sinal>', views.sinal, name='sinal'),
    path('enviarsinais', views.enviarSinais, name='enviarsinais'),
    path('<slug:glossario>/', views.glossarioSelecionado, name='glossarios'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    url('', include('django.contrib.auth.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)