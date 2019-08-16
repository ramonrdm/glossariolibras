# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, redirect
from glossario.models import Glossario, Sinal, Tema, UserGlossario, Localizacao, CM
from django.contrib.auth.models import User
from glossario.forms import PesquisaForm, EnviarSinaisForm, PesquisaSinaisForm, CustomUserCreationForm
from django.http import JsonResponse
from django.db.models import Q
from django.template import RequestContext
import json
import datetime
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.conf import settings
from django.contrib.auth.decorators import login_required

def index(request, glossario=None):
<<<<<<< HEAD
    glossarios = Glossario.objects.filter(visivel=True)
=======
    glossarios = Glossario.objects.all()
    # cm = CM.objects.all()
    # cmGrupos = [c.group for c in cm]
    # cmGrupos = list(dict.fromkeys(cmGrupos))
    print(cmGrupos)
>>>>>>> WidgetCM
    if request.method == 'POST':
        sinais = None
        formPesquisa = PesquisaForm(request.POST)
        formSinais = PesquisaSinaisForm(request.POST)
        if formPesquisa.is_valid() and formSinais.is_valid():
            sinais = busca(formSinais, formPesquisa).filter(glossario__visivel=True)
        formPesquisa = PesquisaForm()
        resultado = len(sinais) if sinais else None

        movimentacoes = dict(
            [('0', 'X.svg'), ('1', 'parede.png'), ('2', 'chao.png'), ('3', 'circular.png'), ('4', 'contato.png')])

        if sinais:
            for sinal in sinais:
                sinal.localizacao = "/static/img/" + Localizacao.localizacoes_imagens[sinal.localizacao]
                sinal.movimentacao = "/static/img/" + movimentacoes[sinal.movimentacao]
        return render(request, 'pesquisa.html', {
             'formPesquisa': formPesquisa, 'sinais': sinais, 'resultado': resultado,
            'formSinais': formSinais, 'form': EnviarSinaisForm(request.POST, request.FILES)})
    else:
        formSinais = PesquisaSinaisForm(request.session) if request.session.get('sinaisCheckboxes') else PesquisaSinaisForm()
        formPesquisa = PesquisaForm()

    return render(request, 'index.html', {'CM': cmGrupos, 'glossarios': glossarios, 'glossario': glossario, 'formPesquisa': formPesquisa,
         'formSinais': formSinais, 'form': EnviarSinaisForm(request.POST, request.FILES)
        })

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

        return render(request, 'glossario.html', {'glossario': glossario, 'formPesquisa': formPesquisa, 'formSinais': formSinais, 'form': EnviarSinaisForm(request.POST, request.FILES)
            })

def sinal(request, sinal=None, glossario=None):
    if sinal:
        try:
            sinal = Sinal.objects.get(id=sinal)
            glossario = sinal.glossario
            sinal.localizacao = "/static/img/"+Localizacao.localizacoes_imagens[sinal.localizacao]

            movimentacoes = dict([('0', 'X.svg'), ('1', 'parede.png'), ('2', 'chao.png'), ('3', 'circular.png'), ('4', 'contato.png')])
            sinal.movimentacao = "/static/img/" + movimentacoes[sinal.movimentacao]

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
        return render(request, "sinal.html", {'sinal': sinal, 'glossario': glossario, 'formPesquisa': formPesquisa,'formSinais': formSinais })

def historia(request):
    return render(request, "historia.html")

def equipe(request):
    usuarios = UserGlossario.objects.all()
    return render(request, "equipe.html", {'usuarios': usuarios})

def contato(request):

    return render(request, "contato.html", {'test': settings.TESTE_USER_DB})

def temas(request, temas=None):
    global queryTemas
    queryTemas = Tema.objects.all()
    try:
        raiz = criaNodo(queryTemas.get(temaPai=None))
        mostraNodo(raiz, 0)
    except Tema.DoesNotExist:
        raiz = None
    return render(request, "temas.html", dict(raiz=raiz))

@login_required
def enviarSinais(request):
    formSinais = EnviarSinaisForm
    cm = CM.objects.all()
    cmGrupos = [c.group for c in cm]
    print( cmGrupos)
    if request.method == 'POST':
        toastSucesso = True
        try:
            if formSinais.is_valid():
                dados = formSinais.save(commit=False)
                dados.glossario = Glossario.objects.get(nome='Sugestões')
                dados.create_data = datetime.date.today()
                if request.FILES.get('sinalLibras'):
                    dados.sinalLibras = request.FILES['sinalLibras']
                if request.FILES.get('descLibras'):
                    dados.descLibras = request.FILES['descLibras']
                if request.FILES.get('exemploLibras'):
                    dados.exemploLibras = request.FILES['exemploLibras']
                if request.FILES.get('varicLibras'):
                    dados.varicLibras = request.FILES['varicLibras']
                dados.save()
                formSinais = EnviarSinaisForm()
                return render(request, 'enviarsinais.html', {'formSinais': formSinais, 'toastSucesso': toastSucesso})
        except ValueError:
            toastRepetido = True
            return render(request, 'enviarsinais.html', {'formSinais': formSinais, 'toastRepetido': toastRepetido})
    else:
        return render(request, 'enviarsinais.html', {'formSinais': formSinais, 'CM': cmGrupos,})

def criaNodo(nodoPai):
    filhosPai = queryTemas.filter(temaPai=nodoPai)
    filhos = list()
    for filho in filhosPai:
        filhos.append(criaNodo(filho))
    nodoPai.filhos = filhos
    return nodoPai

#Metodo simples para exibição da lista no terminal
def mostraNodo(nodoTema1, n):
    txt = " - "*n
    if nodoTema1.filhos:
        print( str(n) + txt +nodoTema1.nome)
        filhos = nodoTema1.filhos
        for filho in filhos:
            mostraNodo(filho, n+1)
    else:
        print (str(n) + txt +nodoTema1.nome)

def mostraNodoJson(nodoTema1):
    if nodoTema1.filhos:
        filhos = nodoTema1.filhos
        jsonTemas['edges'][nodoTema1.nome] = {}
        for filho in filhos:
            mostraNodoJson(filho)
            jsonTemas['edges'][nodoTema1.nome][filho.nome] = {}
    jsonTemas['nodes'][nodoTema1.nome] = {"color":"green", "shape":"dot", "alpha":1, "link":"www.libras.ufsc.br" }

def temasjson(request):
    global jsonTemas
    jsonTemas = {"nodes":{},"edges":{}}
    data = {
        "nodes":{
            "joao" : {"color":"red", "shape":"dot", "alpha":1 },
            "ramon" : {"color":"green", "shape":"dot", "alpha":1, "link":"ramon" },
            "glossario" :{"color":"#b2b19d", "shape":"dot", "alpha":1},
            "NALS" :{"color":"#b2b19d", "shape":"dot", "alpha":1}
        },
        "edges":{
            "glossario":{"joao":{},"ramon":{}}
        }
    }
    data['nodes']['glossario'] = {"color":"green", "shape":"dot", "alpha":1, "link":"ramon" }
    raiz = criaNodo(Tema.objects.get(temaPai=None))
    mostraNodoJson(raiz)
    print (jsonTemas)
    return JsonResponse(jsonTemas)

def busca(formSinais, formPesquisa):
    parametros = {"publicado": True}
    resultadoTraducao = formPesquisa.cleaned_data['busca']
    localizacao = formSinais.cleaned_data['localizacao']
    movimentacao = formSinais.cleaned_data['movimentacao']
    mao = formSinais.cleaned_data['cmE']

    if resultadoTraducao != '':
        sinais = Sinal.objects.filter(Q(traducaoI__icontains=resultadoTraducao) | Q(traducaoP__icontains=resultadoTraducao))

    else:
        if localizacao != '0':
            parametros['localizacao'] = localizacao
        if movimentacao != '0':
            parametros['movimentacao'] = movimentacao

        sinais = Sinal.objects.filter(**parametros)
        if mao:
<<<<<<< HEAD
            sinais = sinais.filter(Q(cmE=formSinais.cleaned_data['cmE']) | Q(cmD=formSinais.cleaned_data['cmE']))
=======
            print(mao)
            sinais = sinais.filter(Q(cmE__bsw__icontains=mao) | Q(cmD__bsw__icontains=mao))
            print("passei aqui 2")
>>>>>>> WidgetCM

    return sinais

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
    return render(request, 'index.html', {'modalConfirmeEmail':modalConfirmeEmail})
