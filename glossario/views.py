# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from glossario.models import Glossario, Sinal, UserGlossario, Localizacao, Movimentacao, Area, Comment
from glossario.forms import PesquisaSinaisForm, CommentForm, SignupForm
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

from django.core.mail import EmailMessage

from django.contrib.postgres.search import SearchVector


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Ative sua conta Glossário Libras'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'registration/email_confirmation_message.html')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserGlossario.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserGlossario.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'registration/email_link_valid.html')
    else:
        return render(request, 'registration/email_link_invalid.html')

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

        formSinais = PesquisaSinaisForm(request.GET)

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

# def pesquisa(request, area=None, query=None, glossario=None):
def pesquisa(request):
    # area = request.GET.get('area', None)
    # glossario = request.GET.get('glossario', None)

    sinais = None
    # glossario = None
    area = None
    formSinais = PesquisaSinaisForm(request.GET)

    # if area:
    #     area = get_object_or_404(Area, slug=area)

    # if glossario:
    #     glossario = get_object_or_404(Glossario, nome=glossario)


    if formSinais.is_valid():
        print("##########################")
        sinais = busca(formSinais, request).filter(glossario__visivel=True)
        glossario = formSinais.cleaned_data['glossario']
        area = formSinais.cleaned_data['area']
        letra_inicial = request.GET.get('letra_inicial', None)

    resultado = len(sinais) if sinais else None

    paginator = Paginator(sinais, 5)
    page = request.GET.get('page')

    try:
        sinais_page = paginator.page(page)
    except PageNotAnInteger:
        sinais_page = paginator.page(1)
    except EmptyPage:
        sinais_page = paginator.page(paginator.num_pages)


    glossarios = Glossario.objects.filter(visivel=True)
    areas = Area.objects.all()
    alfabeto = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
                'n','o','p','q','r','s','t','u','v','w','x','y','z']

    context = { 
        'glossario' : glossario,
        'sinais_page': sinais_page, 
        'resultado': resultado,
        'area': area,
        'formSinais': formSinais,
        'glossarios': glossarios,
        'areas':areas,
        'alfabeto':alfabeto,
        'letra_inicial':letra_inicial,
    }
    return render(request, 'glossario/pesquisa.html', context)

def busca_na_area(area):
    query = Q()
    areas = Area.objects.filter(id=area).get_descendants(include_self=True)
    for _area in areas:
        query |= Q(glossario__area=_area)
    return Sinal.objects.filter(query, publicado=True)

def busca(formSinais, request):
    class Meta:
        ordering = ["-created_date"]

    letra_inicial = request.GET.get('letra_inicial', None)
    area = request.GET.get('area', None)
    glossario = request.GET.get('glossario', None)

    resultadoTraducao = formSinais.cleaned_data['busca']
    localizacao = formSinais.cleaned_data['localizacao']
    movimentacao = formSinais.cleaned_data['movimentacao']
    mao = formSinais.cleaned_data['cmE']
    # glossario = formSinais.cleaned_data['glossario']
    # area = formSinais.cleaned_data['area']
    sinais = Sinal.objects.filter(publicado=True)

    query = Q()

    if area != None and area != '':
        # Gera erro 404 se não existir
        get_object_or_404(Area, id=area)

        areas = Area.objects.filter(id=area).get_descendants(include_self=True)
        for _area in areas:
            query |= Q(glossario__area=_area)

    if glossario != '' and glossario != None:
        # Gera erro 404 se não existir
        get_object_or_404(Glossario, id=glossario)
        query |= Q(id=glossario)
        # sinais = sinais.filter(id=glossario)
    sinais = Sinal.objects.filter(query, publicado=True)

    # Pesquisa por texto
    if resultadoTraducao != '':
        sinais = sinais.annotate(
            search = SearchVector('portugues', 'ingles','descricao'),
        ).filter(search=resultadoTraducao)
    # Utiliza startswith para letras inicial selecionada
    elif letra_inicial != None:
        sinais = sinais.filter(Q(portugues__istartswith=letra_inicial) | Q(
            ingles__istartswith=letra_inicial))
    # Pesquisa por sinal
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
            # Create Comment object but don't save to database yet
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
        return render(request, 'glossario/pesquisa.html', context)
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
    # sinais_relacionados = Sinal.objects.exclude(id=sinal.id).filter(publicado=True)

    related_palavras = sinal.portugues.split()
    for palavra in related_palavras:    
        sinais_relacionados = Sinal.objects.annotate(
            search = SearchVector('portugues', 'ingles','descricao'),
        ).exclude(id=sinal.id).filter(publicado=True, search=palavra)[:5]

    # sinais_relacionados = sinais_relacionados.filter(
    #     Q(localizacao=sinal.localizacao) |
    #     Q(cmE=sinal.cmE) |
    #     Q(cmD=sinal.cmD) |
    #     Q(movimentacao=sinal.movimentacao)
    # )[:5]
        
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
    sinais = Sinal.objects.all().order_by("id")
    url_base = settings.MEDIA_ROOT
    pasta_sinal_preview = '{0}/sinal_preview'.format(url_base)

    # Verifica se a pasta sinal_preview existe
    if not os.path.exists(pasta_sinal_preview):
        os.makedirs(pasta_sinal_preview)
    
    # Atualiza url dos glossarios
    glossarios = Glossario.objects.all()

    for glossario in glossarios:
        gLink = 'glossario/' + slugify(glossario.nome)
        glossario.link = gLink
        glossario.save()

    for sinal in sinais:
        if not sinal.video_sinal:
            continue
        if sinal.preview1:
            continue
        preview_fields = [sinal.preview1, sinal.preview2,
                          sinal.preview3, sinal.preview4]

        arquivo_video_converter = str(url_base) +"/"+ str(sinal.video_sinal)

        # Pega o numero total de frames do video
        output = subprocess.run("ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames -of default=nokey=1:noprint_wrappers=1 {0}".format(
            arquivo_video_converter
        ), capture_output=True, shell=True, check=False)
        
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

    # For debug
    # duplicar modelos existentes
    for _ in range (0,200):
        sinal = Sinal.objects.get(pk=1)
        sinal.pk = None
        sinal.save()

    return render(request, 'glossario/contato.html')