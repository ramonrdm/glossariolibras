# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from glossario.models import Glossario, Sinal, UserGlossario, Localizacao, Movimentacao
from glossario.forms import PesquisaForm, PesquisaSinaisForm, CustomUserCreationForm
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
    if request.method == 'POST':
        sinais = None
        formPesquisa = PesquisaForm(request.POST)
        formSinais = PesquisaSinaisForm(request.POST)

        if formPesquisa.is_valid() and formSinais.is_valid():
            sinais = busca(formSinais, formPesquisa).filter(glossario__visivel=True)
        formPesquisa = PesquisaForm()
        resultado = len(sinais) if sinais else None

        if sinais:
            for sinal in sinais:
                if sinal.localizacao:
                    sinal.localizacao = "/static/img/" + Localizacao.localizacoes_imagens[sinal.localizacao]
                if sinal.movimentacao:
                    sinal.movimentacao = "/static/img/" + Movimentacao.movimentacoes_imagens[sinal.movimentacao]

        page = request.GET.get('page', 1)
        paginator = Paginator(sinais, 5)

        try:
            sinais_page = paginator.page(page)
        except PageNotAnInteger:
            sinais_page = paginator.page(1)
        except EmptyPage:
            sinais_page = paginator.page(paginator.num_pages)
        return render(request, 'pesquisa.html', {
            'formPesquisa': formPesquisa, 'sinais_page': sinais_page, 'resultado': resultado,
            'formSinais': formSinais})
    else:
        formSinais = PesquisaSinaisForm()
        formPesquisa = PesquisaForm()

    return render(request, 'index.html', {'glossarios': glossarios, 'glossario': glossario, 'formPesquisa': formPesquisa,
         'formSinais': formSinais,
    })

def busca(formSinais, formPesquisa):

    resultadoTraducao = formPesquisa.cleaned_data['busca']
    localizacao = formSinais.cleaned_data['localizacao']
    movimentacao = formSinais.cleaned_data['movimentacao']
    mao = formSinais.cleaned_data['cmE']
    sinais = Sinal.objects.filter(publicado=True)
    if resultadoTraducao != '':
        sinais = sinais.filter(Q(portugues__icontains=resultadoTraducao) | Q(ingles__icontains=resultadoTraducao))
    else:
        if localizacao:
            sinais = sinais.filter(localizacao=localizacao)
        if movimentacao:
            sinais = sinais.filter(movimentacao=movimentacao)
        if mao:
            sinais = sinais.filter(Q(cmE=mao) | Q(cmD=mao))
    return sinais

def glossarioSelecionado(request, glossario):
    try:
        glossario = Glossario.objects.get(link=glossario)
    except Glossario.DoesNotExist:
        glossario = None

    if request.method == 'POST':
        sinais = None
        formPesquisa = PesquisaForm(request.POST)
        formSinais = PesquisaSinaisForm(request.POST)

        if formPesquisa.is_valid() and formSinais.is_valid():
            sinais = busca(formSinais, formPesquisa).filter(glossario=glossario, glossario__visivel=True)

        formPesquisa = PesquisaForm()
        resultado = len(sinais) if sinais else None
        movimentacoes = dict(
            [('0', 'X.svg'), ('1', 'parede.png'), ('2', 'chao.png'), ('3', 'circular.png'), ('4', 'contato.png')])

        for sinal in sinais:
            sinal.localizacao = "/static/img/" + Localizacao.localizacoes_imagens[sinal.localizacao]
            sinal.movimentacao = "/static/img/" + movimentacoes[sinal.movimentacao]

        return render(request, 'pesquisa.html', {
            'formPesquisa': formPesquisa, 'sinais': sinais, 'resultado': resultado, 'glossario':
            glossario,
            'formSinais': formSinais
            })
    else:
        formSinais = PesquisaSinaisForm(request.session) if request.session.get('sinaisCheckboxes') else PesquisaSinaisForm()
        # formSinais = PesquisaSinaisForm()
        formPesquisa = PesquisaForm()

        return render(request, 'glossario.html', {'glossario': glossario, 'formPesquisa': formPesquisa, 'formSinais': formSinais
            })

def sinal(request, sinal=None, glossario=None):
    if sinal:
        try:
            sinal = Sinal.objects.get(id=sinal)
            glossario = sinal.glossario
            sinal.localizacao = "/static/img/"+Localizacao.localizacoes_imagens[sinal.localizacao]
            if sinal.movimentacao:
                sinal.movimentacao = "/static/img/" + Movimentacao.movimentacoes_imagens[sinal.movimentacao]

        except Sinal.DoesNotExist:
            sinal = None

    if request.method == 'POST':
        sinais = sinaisGlossario = None
        formPesquisa = PesquisaForm(request.POST)
        request.session['sinaisCheckboxes'] = request.POST.copy()
        formSinais = PesquisaSinaisForm(request.session)
        if formPesquisa.is_valid() and formSinais.is_valid():
            sinaisGlossario = Sinal.objects.filter(glossario=glossario).filter(publicado=True)
        formPesquisa = PesquisaForm()
        resultado = len(sinais) if sinais else None
        return render(request, 'pesquisa.html', {'formPesquisa': formPesquisa, 'sinais': sinais, 'sinaisGlossario': sinaisGlossario, 'resultado': resultado, 'glossario':
            glossario, 'formSinais': formSinais, })
    else:
        formPesquisa = PesquisaForm()
        formSinais = PesquisaSinaisForm()
        return render(request, "sinal.html", {'sinal': sinal, 'glossario': glossario, 'formPesquisa': formPesquisa,'formSinais': formSinais, })

def historia(request):
    return render(request, "historia.html")

def equipe(request):
    return render(request, "equipe.html", {})

def contato(request):

    return render(request, "contato.html")

def registration(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            return redirect('account_activation_sent')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration.html', {'form': form})

def sair(request):
    logout(request)
    return render(request, 'index.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserGlossario.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserGlossario.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_staff = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        modalLogin = True
        return render(request, 'index.html', {'modalLogin': modalLogin})
    else:
        modalConfirmeEmailErro = True
        return render(request, 'index.html', {'modalConfirmeEmailErro': modalConfirmeEmailErro})

def account_activation_sent(request):
    modalConfirmeEmail = True
    return render(request, 'index.html', {'modalConfirmeEmail': modalConfirmeEmail})
