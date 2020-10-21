# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from glossario.models import Glossario, Sinal, UserGlossario, Localizacao, Movimentacao, Area, Comment
from glossario.forms import PesquisaSinaisForm, CommentForm
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


def index(request, glossario=None):
    glossarios = Glossario.objects.filter(visivel=True)
    areas = Area.objects.all()
    area = None
    formSinais = PesquisaSinaisForm()
    sinais_pub = Sinal.objects.filter(publicado=True).count()

    return render(request, 'glossario/index.html', {'glossarios': glossarios, 'glossario': glossario,'areas':areas, 'area':area, 'formSinais': formSinais, 'sinais_pub': sinais_pub})


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

        return render(request, 'glossario/pesquisa.html', {
            'sinais': sinais,
            'resultado': resultado,
            'glossario': glossario,
            'formSinais': formSinais
        })
    else:
        formSinais = PesquisaSinaisForm(request.session) if request.session.get(
            'sinaisCheckboxes') else PesquisaSinaisForm()

        return render(request, 'glossario/glossario.html', {'glossario': glossario, 'glossarios_relacionados':glossarios_relacionados, 'formSinais': formSinais})


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

    if resultadoTraducao != '':
        sinais = sinais.filter(Q(portugues__unaccent__icontains=resultadoTraducao) | Q(
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
            # Create Comment object but don't save to database yet
            novo_comentario = form_comentario.save(commit=False)
            novo_comentario.usuario = usuario
            novo_comentario.sinal = sinal
            novo_comentario.save()

            sinais_relacionados = get_sinais_relacionados(sinal)
            formSinais = PesquisaSinaisForm()
            form_comentario = CommentForm()
            return render(request, "glossario/sinal.html", {'sinal': sinal,'glossario': glossario,
                'formSinais': formSinais, 'sinais_relacionados':sinais_relacionados,
                'form_comentario': form_comentario, 'comentarios': comentarios})

        resultado = len(sinais) if sinais else None
        return render(request, 'glossario/pesquisa.html', {'sinais': sinais,
            'sinaisGlossario': sinaisGlossario, 'resultado': resultado, 'glossario': glossario,
            'formSinais': formSinais, 'form_comentario': form_comentario})
    else:
        # Procura sinais relacionados
        sinais_relacionados = get_sinais_relacionados(sinal)
        formSinais = PesquisaSinaisForm()
        form_comentario = CommentForm()
        return render(request, "glossario/sinal.html", {'sinal': sinal,'glossario': glossario,
            'formSinais': formSinais, 'sinais_relacionados':sinais_relacionados,
            'form_comentario': form_comentario, 'comentarios': comentarios})

def get_sinais_relacionados(sinal):
    sinais_relacionados = Sinal.objects.exclude(id=sinal.id).filter(publicado=True)

    # Palavras semelhantes portugues
    query_pt = Q()
    related_palavras = sinal.portugues.split()
    for palavra in related_palavras:
        query_pt |= Q(portugues__unaccent__icontains=palavra)

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
    )
        
    return sinais_relacionados

def historia(request):
    return render(request, "glossario/historia.html")


def equipe(request):
    return render(request, "glossario/equipe.html", {})


def contato(request):
    return render(request, "glossario/contato.html")


def sair(request):
    logout(request)
    return render(request, 'glossario/index.html')
