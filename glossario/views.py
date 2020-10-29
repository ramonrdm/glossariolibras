# -*- coding: utf-8 -*-
from django.http import HttpResponse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from glossario.models import Glossario, Sinal, UserGlossario, Localizacao, Movimentacao, Area, Comment
from glossario.forms import PesquisaSinaisForm, CommentForm, CustomRegistrationForm
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.generic.edit import FormView


import subprocess
import math
from django.conf import settings
import os
from django.template.defaultfilters import slugify

from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import View

from django.core.mail import EmailMessage
from django.contrib import messages

class SignUpView(generic.CreateView):
    form_class = CustomRegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            # user.save()

            current_site = get_current_site(request)
            mail_subject = 'Ativar sua conta Glossario'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            user.save()
            # user.email_user(subject, message)

            messages.success(request, ('Please Confirm your email to complete registration.'))

            return redirect('login')

        return render(request, self.template_name, {'form': form})

class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = UserGlossario.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserGlossario.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('index')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('index')

# def signup(request):
#     if request.method == 'POST':
#         form = CustomRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             current_site = get_current_site(request)
#             mail_subject = 'Ativar sua conta Glossario'
#             message = render_to_string('registration/account_activation_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token':account_activation_token.make_token(user),
#             })
#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(
#                         mail_subject, message, to=[to_email]
#             )
#             email.send()
#             user.save()
#             return HttpResponse('Please confirm your email address to complete the registration')
#     else:
#         form = CustomRegistrationForm()
#     return render(request, 'registration/signup.html', {'form': form})

# def activate(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = UserGlossario.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, UserGlossario.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         # return redirect('home')
#         return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
#     else:
#         return HttpResponse('Activation link is invalid!')

def index(request, glossario=None):
    glossarios = Glossario.objects.filter(visivel=True)
    areas = Area.objects.all()
    area = None
    formSinais = PesquisaSinaisForm()
    sinais_pub = Sinal.objects.filter(publicado=True).count()

    context = {
        'glossarios': glossarios,
        'glossario': glossario,
        'areas':areas,
        'area':area,
        'formSinais': formSinais,
        'sinais_pub': sinais_pub
    }

    return render(request, 'glossario/index.html', context)


def glossarioSelecionado(request, glossario):
    try:
        glossario = Glossario.objects.get(link='glossario/'+glossario)
        glossarios_relacionados = Glossario.objects.exclude(id=glossario.id).filter(area=glossario.area)
    except Glossario.DoesNotExist:
        glossario = None
        glossarios_relacionados = None

    if request.method == 'POST':
        sinais = None

        formSinais = PesquisaSinaisForm(request.POST)

        if formSinais.is_valid():
            sinais = busca(formSinais).filter(
                glossario=glossario, glossario__visivel=True)

        resultado = len(sinais) if sinais else None

        context = {
            'sinais': sinais,
            'resultado': resultado,
            'glossario': glossario,
            'formSinais': formSinais
        }
        return render(request, 'glossario/pesquisa.html', context)
    else:
        formSinais = PesquisaSinaisForm(request.session) if request.session.get('sinaisCheckboxes') else PesquisaSinaisForm()

        context = {
            'glossario': glossario,
            'formSinais': formSinais,
            'glossarios_relacionados': glossarios_relacionados
        }
        return render(request, 'glossario/glossario.html', context)


def pesquisa(request, area=None):
    sinais = None
    glossario = None
    formSinais = PesquisaSinaisForm(request.POST)

    if area:
        area = Area.objects.get(slug=area)

    # Pesquisa normal
    if request.method == 'POST':
        if formSinais.is_valid():
            sinais = busca(formSinais).filter(glossario__visivel=True)
            glossario = formSinais.cleaned_data['glossario']
            area = formSinais.cleaned_data['area']
    # Caso o usuario selecione a area
    else:
        sinais = busca_na_area(area)

    resultado = len(sinais) if sinais else None

    paginator = Paginator(sinais, 5)
    page = request.POST.get('page')

    try:
        sinais_page = paginator.page(page)
    except PageNotAnInteger:
        sinais_page = paginator.page(1)
    except EmptyPage:
        sinais_page = paginator.page(paginator.num_pages)

    context = { 
                'glossario' : glossario,
                'sinais_page': sinais_page, 
                'resultado': resultado,
                'area': area,
                'formSinais': formSinais
    }
    return render(request, 'glossario/pesquisa.html', context)

def busca_na_area(area):
    query = Q()
    areas = Area.objects.filter(id=area.id).get_descendants(include_self=True)
    for _area in areas:
        query |= Q(glossario__area=_area)
    return Sinal.objects.filter(query)

def busca(formSinais):
    class Meta:
        ordering = ["-created_date"]

    resultadoTraducao = formSinais.cleaned_data['busca']
    localizacao = formSinais.cleaned_data['localizacao']
    movimentacao = formSinais.cleaned_data['movimentacao']
    mao = formSinais.cleaned_data['cmE']
    glossario = formSinais.cleaned_data['glossario']
    area = formSinais.cleaned_data['area']
    sinais = Sinal.objects.filter(publicado=True)

    if area != None:
        sinais = busca_na_area(area)
    elif glossario != None:
        sinais = sinais.filter(glossario=glossario)
    # Tratar busca sem acento
    if resultadoTraducao != '':
        sinais = sinais.filter(Q(portugues__icontains=resultadoTraducao) | Q(
            ingles__icontains=resultadoTraducao))
    else:
    # Se o campo for nulo ignora ele na pesquisa
        if localizacao:
            if localizacao != '0':
                sinais = sinais.filter(localizacao=localizacao)

        if movimentacao:
            if movimentacao != '0':
                sinais = sinais.filter(movimentacao=movimentacao)
        if mao:
            if mao.group != "Nenhum":
                sinais = sinais.filter(Q(cmE=mao) | Q(cmD=mao))
    return sinais    

def sinal(request, sinal=None, glossario=None):
    if sinal:
        try:
            sinal = Sinal.objects.get(id=sinal)
            glossario = sinal.glossario
            comentarios = sinal.comments.filter(ativo=True)

        except Sinal.DoesNotExist:
            sinal = None
            comentarios = None

    if request.method == 'POST':
        sinais = sinaisGlossario = None
        request.session['sinaisCheckboxes'] = request.POST.copy()
        
        # Pesquisa
        formSinais = PesquisaSinaisForm(request.session)
        if formSinais.is_valid():
            sinaisGlossario = Sinal.objects.filter(
                glossario=glossario).filter(publicado=True)
        # Comentarios
        form_comentario = CommentForm(data=request.POST)
        if form_comentario.is_valid():
            if request.user.is_authenticated:
                usuario = request.user
            # Cria objeto comentario sem salvar
            novo_comentario = form_comentario.save(commit=False)
            novo_comentario.usuario = usuario
            novo_comentario.sinal = sinal
            novo_comentario.save()

            sinais_relacionados = get_sinais_relacionados(sinal)
            formSinais = PesquisaSinaisForm()
            form_comentario = CommentForm()

            context = {
                'glossario': glossario,
                'formSinais': formSinais,
                'form_comentario': form_comentario,
                'sinal': sinal,
                'sinais_relacionados':sinais_relacionados,
                'comentarios': comentarios
            }
            return render(request, "glossario/sinal.html", context)

        resultado = len(sinais) if sinais else None
        context = {
            'glossario': glossario,
            'formSinais': formSinais,
            'form_comentario': form_comentario,
            'sinais': sinais,
            'sinaisGlossario': sinaisGlossario,
            'resultado': resultado,
        }
        return render(request, 'glossario/pesquisa.html', )
    else:
        # Procura sinais relacionados
        sinais_relacionados = get_sinais_relacionados(sinal)
        formSinais = PesquisaSinaisForm()
        form_comentario = CommentForm()

        context = {
            'glossario': glossario,
            'formSinais': formSinais,
            'form_comentario': form_comentario,
            'sinal': sinal,
            'sinais_relacionados':sinais_relacionados,
            'comentarios': comentarios
        }
        return render(request, "glossario/sinal.html", context)

def get_sinais_relacionados(sinal):
    sinais_relacionados = Sinal.objects.exclude(id=sinal.id).filter(publicado=True)

    # Palavras semelhantes portugues
    query_pt = Q()
    related_palavras = sinal.portugues.split()
    # Tratar busca sem acento
    for palavra in related_palavras:
        query_pt |= Q(portugues__icontains=palavra)

    # Palavras semelhantes ingles
    query_en = Q()
    if sinal.ingles:
        related_palavras = sinal.ingles.split()
        for palavra in related_palavras:
            query_en |= Q(ingles__icontains=palavra)

    sinais_relacionados = sinais_relacionados.filter(
        query_pt |
        query_en |
        Q(localizacao=sinal.localizacao) |
        Q(cmE=sinal.cmE) |
        Q(cmD=sinal.cmD) |
        Q(movimentacao=sinal.movimentacao)
    )[:5]
        
    return sinais_relacionados

def historia(request):
    sinais_publicados = Sinal.objects.filter(publicado=True).count()
    sinais_totais = Sinal.objects.all().count()

    context = {
        'sinais_publicados': sinais_publicados,
        'sinais_totais': sinais_totais
    }
    return render(request, "glossario/historia.html", context)


def equipe(request):
    return render(request, "glossario/equipe.html", {})


def contato(request):
    return render(request, "glossario/contato.html")


def sair(request):
    logout(request)
    return render(request, 'glossario/index.html')

def update(request):
    # Atualiza preview dos sinais
    sinais = Sinal.objects.all()
    url_base = settings.MEDIA_ROOT
    pasta_sinal_preview = '{0}/sinal_preview'.format(url_base)

    # Verifica se a pasta sinal_preview existe
    if not os.path.exists(pasta_sinal_preview):
        os.makedirs(pasta_sinal_preview)

    for sinal in sinais:
        preview_fields = [sinal.preview1, sinal.preview2,
                          sinal.preview3, sinal.preview4]

        arquivo_video_converter = str(url_base) +"/"+ str(sinal.video_sinal)

        # Pega o numero total de frames do video
        output = subprocess.run("ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames -of default=nokey=1:noprint_wrappers=1 {0}".format(
            arquivo_video_converter
        ), capture_output=True, shell=True, check=False)
        output.wait()
        duration = output.stdout.decode()

        # duracao menos 60 para remover a soma dos frames inicias com os finais
        duration_preview = math.ceil((int(duration)-60)/4)

        nome_preview = str(sinal.id)+"-preview%3d.png"
        arquivo_preview = pasta_sinal_preview+'/'+nome_preview
        # valor 15 para pular os primeiros frames
        subprocess.call("ffmpeg -i {0} -vf select='between(n\,15\,{1})*not(mod(n\,{2}))' -vsync vfr {3}".format(
            arquivo_video_converter, int(duration)-45,duration_preview, arquivo_preview), shell=True)
        # Atualiza path dos preview
        for i, preview in enumerate(preview_fields):
            nome_relativo_preview = "sinal_preview/" + \
                str(sinal.id)+"-preview00"+str(i+1)+".png"
            Sinal.objects.filter(id=sinal.id).update(
                **{"%s" % preview.field.name: nome_relativo_preview}
            )
    # Atualiza url dos glossarios
    glossarios = Glossario.objects.all()

    for glossario in glossarios:
        gLink = 'glossario/' + slugify(glossario.nome)
        glossario.link = gLink
        glossario.save()

    return render(request, 'glossario/contato.html')