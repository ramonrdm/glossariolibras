# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from glossario.models import Glossario, Sinal, UserGlossario, Localizacao, Movimentacao
from glossario.forms import PesquisaSinaisForm
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


def index(request, glossario=None):
    glossarios = Glossario.objects.filter(visivel=True)
    formSinais = PesquisaSinaisForm()

    return render(request, 'glossario/index.html', {'glossarios': glossarios, 'glossario': glossario, 'formSinais': formSinais})


def glossarioSelecionado(request, glossario):
    try:
        glossario = Glossario.objects.get(link=glossario)
        print("Glossario: ", glossario)
    except Glossario.DoesNotExist:
        glossario = None

    if request.method == 'POST':
        sinais = None

        formSinais = PesquisaSinaisForm(request.POST)

        if formSinais.is_valid():
            sinais = busca(formSinais).filter(
                glossario=glossario, glossario__visivel=True)

        resultado = len(sinais) if sinais else None
        movimentacoes = dict(
            [('0', 'X.svg'), ('1', 'parede.png'), ('2', 'chao.png'), ('3', 'circular.png'), ('4', 'contato.png')])

        for sinal in sinais:
            sinal.localizacao = "/static/img/" + \
                Localizacao.localizacoes_imagens[sinal.localizacao]
            sinal.movimentacao = "/static/img/" + \
                movimentacoes[sinal.movimentacao]

        return render(request, 'glossario/pesquisa.html', {
            'sinais': sinais, 'resultado': resultado, 'glossario':
            glossario,
            'formSinais': formSinais
        })
    else:
        formSinais = PesquisaSinaisForm(request.session) if request.session.get(
            'sinaisCheckboxes') else PesquisaSinaisForm()
        # formSinais = PesquisaSinaisForm()

        return render(request, 'glossario/glossario.html', {'glossario': glossario, 'formSinais': formSinais
                                                            })


def pesquisa(request):
    if request.method == 'POST':
        sinais = None
        formSinais = PesquisaSinaisForm(request.POST)

        if formSinais.is_valid():
            sinais = busca(formSinais).filter(glossario__visivel=True)
            glossario = formSinais.cleaned_data['glossario']

        resultado = len(sinais) if sinais else None

        if sinais:
            for sinal in sinais:
                if sinal.localizacao:
                    sinal.localizacao = "/static/img/" + \
                        Localizacao.localizacoes_imagens[sinal.localizacao]
                if sinal.movimentacao:
                    sinal.movimentacao = "/static/img/" + \
                        Movimentacao.movimentacoes_imagens[sinal.movimentacao]

        paginator = Paginator(sinais, 5)
        page = request.POST.get('page')

        try:
            sinais_page = paginator.page(page)
        except PageNotAnInteger:
            sinais_page = paginator.page(1)
        except EmptyPage:
            sinais_page = paginator.page(paginator.num_pages)

        context = {
            'glossario': glossario,
            'sinais_page': sinais_page,
            'resultado': resultado,
            'formSinais': formSinais
        }
        return render(request, 'glossario/pesquisa.html', context)


def busca(formSinais):

    resultadoTraducao = formSinais.cleaned_data['busca']
    localizacao = formSinais.cleaned_data['localizacao']
    movimentacao = formSinais.cleaned_data['movimentacao']
    mao = formSinais.cleaned_data['cmE']
    glossario = formSinais.cleaned_data['glossario']
    sinais = Sinal.objects.filter(publicado=True)
    print("glossario:", glossario)

    if glossario != None:
        sinais = sinais.filter(glossario=glossario)

    if resultadoTraducao != '':
        sinais = sinais.filter(Q(portugues__icontains=resultadoTraducao) | Q(
            ingles__icontains=resultadoTraducao))
    else:
        if localizacao:
            sinais = sinais.filter(localizacao=localizacao)
        if movimentacao:
            sinais = sinais.filter(movimentacao=movimentacao)
        if mao:
            sinais = sinais.filter(Q(cmE=mao) | Q(cmD=mao))
    return sinais

    class Meta:
        ordering = ["-created_date"]


def sinal(request, sinal=None, glossario=None):
    if sinal:
        try:
            sinal = Sinal.objects.get(id=sinal)
            glossario = sinal.glossario
            if sinal.localizacao:
                sinal.localizacao = "/static/img/" + \
                    Localizacao.localizacoes_imagens[sinal.localizacao]
            if sinal.movimentacao:
                sinal.movimentacao = "/static/img/" + \
                    Movimentacao.movimentacoes_imagens[sinal.movimentacao]

        except Sinal.DoesNotExist:
            sinal = None

    if request.method == 'POST':
        sinais = sinaisGlossario = None

        request.session['sinaisCheckboxes'] = request.POST.copy()
        formSinais = PesquisaSinaisForm(request.session)
        if formSinais.is_valid():
            sinaisGlossario = Sinal.objects.filter(
                glossario=glossario).filter(publicado=True)

        resultado = len(sinais) if sinais else None
        return render(request, 'glossario/pesquisa.html', {'sinais': sinais, 'sinaisGlossario': sinaisGlossario, 'resultado': resultado, 'glossario':
                                                           glossario, 'formSinais': formSinais, })
    else:

        formSinais = PesquisaSinaisForm()
        return render(request, "glossario/sinal.html", {'sinal': sinal, 'glossario': glossario, 'formSinais': formSinais, })


def historia(request):
    return render(request, "glossario/historia.html")


def equipe(request):
    return render(request, "glossario/equipe.html", {})


def contato(request):

    return render(request, "glossario/contato.html")


def sair(request):
    logout(request)
    return render(request, 'glossario/index.html')
