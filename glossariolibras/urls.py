from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from glossario import views
from django.views.static import serve
from django.urls import path
from django.views.generic import RedirectView
from django.urls import reverse
from django.shortcuts import redirect
from django_registration.backends.one_step.views import RegistrationView
from glossario.forms import CustomRegistrationForm
from django.conf.urls import url, include

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', lambda _: redirect(to="glossario/sinal/")),
    path('admin/', admin.site.urls),
    path('logout/', views.sair, name='logout'),
    path('equipe', views.equipe, name='equipe'),
    path('pesquisa', views.pesquisa, name='pesquisa'),
    path('pesquisa/<slug:area>', views.pesquisa, name='pesquisa'),
    path('contato', views.contato, name='contato'),
    path('historia', views.historia, name='historia'),
    path('sinal/<int:sinal>', views.sinal, name='sinal'),
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/img/marca_glossario2.png')),
    path('glossario/<slug:glossario>/', views.glossarioSelecionado, name='glossarios'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^accounts/register/',
            RegistrationView.as_view(success_url='/profile/', form_class=CustomRegistrationForm),
            name='django_registration_register'),
    url(r'^accounts/login/$', RedirectView.as_view(url='/admin/login/', permanent=True), name='index'),
    url(r'^accounts/', include('django_registration.backends.activation.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    # url para atualizar previews e urls dos glossarios
    path('update',views.update, name='update'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)