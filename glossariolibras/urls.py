from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.conf.urls.static import static
from django.conf import settings
from glossario import views
from django.views.static import serve
from django.urls import path
from django.views.generic import RedirectView
from django.urls import reverse
from django.shortcuts import redirect
from django_registration.backends.one_step.views import RegistrationView
from glossario.forms import SignupForm
from django.conf.urls import url, include

admin.site.login = staff_member_required(admin.site.login, login_url=settings.LOGIN_URL)
admin.site.site_header = 'Administração Glossário Libras'
admin.site.site_title = 'Administração Glossário Libras'

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^admin/login$', RedirectView.as_view(url=settings.LOGIN_URL, permanent=True)),
    path('admin/', lambda _: redirect(to="glossario/sinal/")),
    path('admin/', admin.site.urls),
    path('logout/', views.sair, name='logout'),
    path('equipe', views.equipe, name='equipe'),
    url(r'^pesquisa/$', views.pesquisa, name='pesquisa'),
    # path('pesquisa/<slug:area>', views.pesquisa, name='pesquisa'),
    # path('pesquisa/<slug:glossario>', views.pesquisa, name='pesquisa_glossario'),
    # path('pesquisa/<slug:area>/<slug:glossario>', views.pesquisa, name='pesquisa'),
    # path('pesquisa/<slug:area>/<slug:glossario>/<str:query>', views.pesquisa, name='pesquisa'),
    path('contato', views.contato, name='contato'),
    path('historia', views.historia, name='historia'),
    path('sinal/<int:sinal>', views.sinal, name='sinal'),
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/img/marca_glossario2.png')),
    path('glossario/<slug:glossario>/', views.glossarioSelecionado, name='glossario'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    # url para atualizar previews e urls dos glossarios
    path('update',views.update, name='update'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)