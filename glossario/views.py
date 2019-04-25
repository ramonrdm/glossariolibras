# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, redirect
from glossario.models import Glossario, Sinal, Tema, UserGlossario
from django.contrib.auth.models import User
from glossario.forms import PesquisaForm, PesquisaCheckboxForm, EnviarSinaisForm, PesquisaSinaisForm, CustomUserCreationForm
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
    glossarios = Glossario.objects.all()
    checkboxPort = request.POST.get('checkboxPort', False)
    checkboxIng = request.POST.get('checkboxIng', False)
    request.session['sinaisCheckboxes'] = []

    if request.method == 'POST':
        sinais = sinaisP = sinaisI = sinaisGlossario = formPesquisa = None
        formPesquisa = PesquisaForm(request.POST)
        request.session['sinaisCheckboxes'] = request.POST.copy()
        formCheckbox = PesquisaCheckboxForm(request.session['sinaisCheckboxes'])
        formSinais = PesquisaSinaisForm(request.session['sinaisCheckboxes'])
        # formSinais = PesquisaSinaisForm(request.POST)
        if formPesquisa.is_valid() and formSinais.is_valid():

            parametros = {"publicado": True}
            resultadoTraducao = formPesquisa.cleaned_data['busca']

            if resultadoTraducao != '':
                print('passeia aqui')
                if checkboxIng:
                    parametros["traducaoI__icontains"] = resultadoTraducao
                else:
                    parametros["traducaoP__icontains"] = resultadoTraducao

            else:
                localizacao = int(formSinais.cleaned_data['localizacao'])
                movimentacao = int(formSinais.cleaned_data['movimentacao'])
                grupo = formSinais.cleaned_data['grupoCMe']
                mao = formSinais.cleaned_data['cmE']
                ou = None
                if grupo == None:
                    grupo = 0
                if mao == None:
                    mao = 0

                if localizacao != 0:
                    parametros['localizacao'] = localizacao
                if movimentacao !=  0:
                    parametros['movimentacao'] = movimentacao
                if grupo != 0:
                    #parametros['grupoCMe'] = grupo
                    ou = (Q(grupoCMe=formSinais.cleaned_data['grupoCMe']) | Q(grupoCMd=formSinais.cleaned_data['grupoCMe']))
                if mao !=  0:
                    parametros['cmE'] = mao

            sinais = Sinal.objects.filter(**parametros)
            if ou:
                sinais.filter(ou)


            #sinaisGlossario = Sinal.objects.filter(publicado=True)
            # resultadoTraducao = formPesquisa.cleaned_data['busca'] or []
            # if checkboxPort and checkboxIng:
            #     sinaisP = filterSinaisPort(formSinais, sinaisGlossario, resultadoTraducao)
            #     sinaisI = filterSinaisIng(formSinais, sinaisGlossario, resultadoTraducao)
            # elif checkboxPort and not checkboxIng:
            #     sinais = filterSinaisPort(formSinais, sinaisGlossario, resultadoTraducao)
            # elif checkboxIng and not checkboxPort:
            #     sinais = filterSinaisIng(formSinais, sinaisGlossario, resultadoTraducao)
        formPesquisa = PesquisaForm()
        resultado = len(sinais) if sinais else None
        resultadoP = len(sinaisP) if sinaisP else None
        resultadoI = len(sinaisI) if sinaisI else None
        return render(request, 'pesquisa.html', {
            'formPesquisa': formPesquisa, 'sinais': sinais, 'sinaisP': sinaisP, 'sinaisI': sinaisI,'sinaisGlossario':
            sinaisGlossario, 'resultado': resultado, 'resultadoP': resultadoP, 'resultadoI': resultadoI, 'glossario':
            glossario, 'checkboxPort': checkboxPort, 'checkboxIng': checkboxIng, 'formCheckbox': formCheckbox,
            'formSinais': formSinais, 'form': EnviarSinaisForm(request.POST, request.FILES)})

    else:
        formCheckbox = PesquisaCheckboxForm(request.session['sinaisCheckboxes']) if request.session.get('sinaisCheckboxes')	else PesquisaCheckboxForm()
        formSinais = PesquisaSinaisForm(request.session['sinaisCheckboxes']) if request.session.get('sinaisCheckboxes') else PesquisaSinaisForm()
        # formSinais = PesquisaSinaisForm()
        formPesquisa = PesquisaForm()

    return render(request, 'index.html', {'glossarios': glossarios, 'glossario': glossario, 'formPesquisa': formPesquisa, 'checkboxPort': checkboxPort,
        'checkboxIng': checkboxIng, 'formCheckbox': formCheckbox, 'formSinais': formSinais, 'form': EnviarSinaisForm(request.POST, request.FILES)
        })

def glossarioSelecionado(request, glossario):
    try:
        glossario = Glossario.objects.get(link=glossario)
    except Glossario.DoesNotExist:
        glossario = None

    checkboxPort = request.POST.get('checkboxPort', False)
    checkboxIng = request.POST.get('checkboxIng', False)

    request.session['sinaisCheckboxes'] = []

    if request.method == 'POST':
        sinais = sinaisP = sinaisI = sinaisGlossario = formPesquisa = None
        formPesquisa = PesquisaForm(request.POST)
        request.session['sinaisCheckboxes'] = request.POST.copy()
        formCheckbox = PesquisaCheckboxForm(request.session['sinaisCheckboxes'])
        formSinais = PesquisaSinaisForm(request.session['sinaisCheckboxes'])
        # formSinais = PesquisaSinaisForm(request.POST)
        if formPesquisa.is_valid() and formSinais.is_valid():
            sinaisGlossario = Sinal.objects.filter(glossario=glossario).filter(publicado=True)
            resultadoTraducao = formPesquisa.cleaned_data['busca'] or []
            if checkboxPort and checkboxIng:
                sinaisP = filterSinaisPort(formSinais, sinaisGlossario, resultadoTraducao)
                sinaisI = filterSinaisIng(formSinais, sinaisGlossario, resultadoTraducao)
            elif checkboxPort and not checkboxIng:
                sinais = filterSinaisPort(formSinais, sinaisGlossario, resultadoTraducao)
            elif checkboxIng and not checkboxPort:
                sinais = filterSinaisIng(formSinais, sinaisGlossario, resultadoTraducao)
        formPesquisa = PesquisaForm()
        resultado = len(sinais) if sinais else None
        resultadoP = len(sinaisP) if sinaisP else None
        resultadoI = len(sinaisI) if sinaisI else None
        return render(request, 'pesquisa.html', {
            'formPesquisa': formPesquisa, 'sinais': sinais, 'sinaisP': sinaisP, 'sinaisI': sinaisI,'sinaisGlossario':
            sinaisGlossario, 'resultado': resultado, 'resultadoP': resultadoP, 'resultadoI': resultadoI, 'glossario':
            glossario, 'checkboxPort': checkboxPort, 'checkboxIng': checkboxIng, 'formCheckbox': formCheckbox,
            'formSinais': formSinais
            })
    else:
        formCheckbox = PesquisaCheckboxForm(request.session['sinaisCheckboxes']) if request.session.get('sinaisCheckboxes')	else PesquisaCheckboxForm()
        formSinais = PesquisaSinaisForm(request.session['sinaisCheckboxes']) if request.session.get('sinaisCheckboxes') else PesquisaSinaisForm()
        # formSinais = PesquisaSinaisForm()
        formPesquisa = PesquisaForm()

        return render(request, 'glossario.html', {'glossario': glossario, 'formPesquisa': formPesquisa, 'checkboxPort': checkboxPort,
            'checkboxIng': checkboxIng, 'formCheckbox': formCheckbox, 'formSinais': formSinais, 'form': EnviarSinaisForm(request.POST, request.FILES)
            })

def sinal(request, sinal=None, glossario=None):
    if sinal:
        try:
            sinal = Sinal.objects.get(id=sinal)
            glossario = sinal.glossario
            localizacoes = dict([('1','localizacaoCabeca.png'),('2','localizacaoOmbros.png'),('3','localizacaoBracos.png'),
                                ('4','localizacaoNariz.png'),('5','localizacaoBochechas.png'),('6','localizacaoBoca.png'),
                                ('7','localizacaoTronco.png'),('8','localizacaoNeutro.png'),('9','localizacaoOlhos.png'),('10','localizacaoOrelhas.png'),
                                ('11','localizacaoPescoco.png'),('12','localizacaoQueixo.png'),('13','localizacaoTesta.png')])
            sinal.localizacao = "/static/img/"+localizacoes[sinal.localizacao]

            movimentacoes = dict([('0', 'X.svg'), ('1', 'parede.png'), ('2', 'chao.png'), ('3', 'circular.png'), ('4', 'contato.png')])
            sinal.movimentacao = "/static/img/" + movimentacoes[sinal.movimentacao]

        except Sinal.DoesNotExist:
            sinal = None

    checkboxPort = request.POST.get('checkboxPort', False)
    checkboxIng = request.POST.get('checkboxIng', False)

    if request.method == 'POST':
        sinais = sinaisP = sinaisI = sinaisGlossario = formPesquisa = None
        formPesquisa = PesquisaForm(request.POST)
        request.session['sinaisCheckboxes'] = request.POST.copy()
        formCheckbox = PesquisaCheckboxForm(request.session['sinaisCheckboxes'])
        formSinais = PesquisaSinaisForm(request.session['sinaisCheckboxes'])
        if formPesquisa.is_valid() and formSinais.is_valid():
            sinaisGlossario = Sinal.objects.filter(glossario=glossario).filter(publicado=True)
            resultadoTraducao = formPesquisa.cleaned_data['busca'] or []
            if checkboxPort and checkboxIng:
                sinaisP = filterSinaisPort(formSinais, sinaisGlossario, resultadoTraducao)
                sinaisI = filterSinaisIng(formSinais, sinaisGlossario, resultadoTraducao)
            elif checkboxPort and not checkboxIng:
                sinais = filterSinaisPort(formSinais, sinaisGlossario, resultadoTraducao)
            elif checkboxIng and not checkboxPort:
                sinais = filterSinaisIng(formSinais, sinaisGlossario, resultadoTraducao)
        formPesquisa = PesquisaForm()
        resultado = len(sinais) if sinais else None
        resultadoP = len(sinaisP) if sinaisP else None
        resultadoI = len(sinaisI) if sinaisI else None
        return render(request, 'pesquisa.html', {
            'formPesquisa': formPesquisa, 'sinais': sinais, 'sinaisP': sinaisP, 'sinaisI': sinaisI, 'sinaisGlossario':
            sinaisGlossario, 'resultado': resultado, 'resultadoP': resultadoP, 'resultadoI': resultadoI, 'glossario':
            glossario, 'checkboxPort': checkboxPort,'checkboxIng': checkboxIng, 'formCheckbox': formCheckbox,
            'formSinais': formSinais, })
    else:
        formPesquisa = PesquisaForm()
        formCheckbox = PesquisaCheckboxForm(request.session['sinaisCheckboxes'])
        formSinais = PesquisaSinaisForm(request.session['sinaisCheckboxes'])
        return render(request, "sinal.html", {'sinal': sinal, 'glossario': glossario, 'formPesquisa': formPesquisa,
            'formCheckbox': formCheckbox, 'formSinais': formSinais })

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
    if request.method == 'POST':
        toastSucesso = True
        try:
            if formSinais.is_valid():
                dados = formSinais.save(commit=False)
                dados.glossario = Glossario.objects.get(nome='Sugestões')
                dados.dataPost = datetime.date.today()
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
        return render(request, 'enviarsinais.html', {'formSinais': formSinais })

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

#################### MÉTODOS ####################

def filterSinaisPort(formSinais, sinaisGlossario, resultadoTraducao):

     if resultadoTraducao == []:
         localizacao = int(formSinais.cleaned_data['localizacao'])
         movimentacao = int(formSinais.cleaned_data['movimentacao'])
         grupo = formSinais.cleaned_data['grupoCMe']
         mao = formSinais.cleaned_data['cmE']
         if grupo == None:
             grupo = 0
         if mao == None:
             mao = 0

         print(localizacao)
         print(movimentacao)
         print(grupo)
         print(mao)

         if localizacao == 0 and movimentacao == 0 and grupo == 0 and mao == 0:
            print('PASSEI vazio')
            return None

         elif localizacao != 0 and movimentacao == 0 and grupo == 0 and mao == 0:
             print('PASSEI loc')
             return sinaisGlossario.filter(
                 Q(localizacao=formSinais.cleaned_data['localizacao'])
             ).distinct()

         elif localizacao != 0 and movimentacao != 0 and grupo == 0 and mao == 0:
             print('PASSEI loca + movi')
             return sinaisGlossario.filter(
                 Q(localizacao=formSinais.cleaned_data['localizacao']) &
                 Q(movimentacao=formSinais.cleaned_data['movimentacao'])
             ).distinct()

         elif localizacao != 0 and movimentacao != 0 and grupo != 0 and mao == 0:
             print('PASSEI loca + movi + grupo')
             return sinaisGlossario.filter(
                 Q(localizacao=formSinais.cleaned_data['localizacao']) &
                 Q(movimentacao=formSinais.cleaned_data['movimentacao']) &
                 (Q(grupoCMe=formSinais.cleaned_data['grupoCMe']) | Q(grupoCMd=formSinais.cleaned_data['grupoCMe']))
             ).distinct()

         elif localizacao != 0 and movimentacao != 0 and grupo != 0 and mao != 0:
             print('PASSEI TODOS')
             return sinaisGlossario.filter(
                 Q(localizacao=formSinais.cleaned_data['localizacao']) &
                 Q(movimentacao=formSinais.cleaned_data['movimentacao']) &
                 (Q(grupoCMe=formSinais.cleaned_data['grupoCMe']) | Q(grupoCMd=formSinais.cleaned_data['grupoCMe'])) &
                 (Q(cmE=formSinais.cleaned_data['cmE']) | Q(cmD=formSinais.cleaned_data['cmE']))
             ).distinct()

         elif localizacao == 0 and movimentacao != 0 and grupo == 0 and mao == 0:
             print('PASSEI  movi')
             return sinaisGlossario.filter(
                 Q(movimentacao=formSinais.cleaned_data['movimentacao'])
             ).distinct()

         elif localizacao == 0 and movimentacao != 0 and grupo != 0 and mao == 0:
             print('PASSEI  movi + grupo')
             return sinaisGlossario.filter(
                 Q(movimentacao=formSinais.cleaned_data['movimentacao']) &
                 (Q(grupoCMe=formSinais.cleaned_data['grupoCMe']) | Q(grupoCMd=formSinais.cleaned_data['grupoCMe']))
             ).distinct()

         elif localizacao == 0 and movimentacao != 0 and grupo != 0 and mao != 0:
             print('PASSEI  movi + grupo + mao')
             return sinaisGlossario.filter(
                 Q(movimentacao=formSinais.cleaned_data['movimentacao']) &
                 (Q(grupoCMe=formSinais.cleaned_data['grupoCMe']) | Q(grupoCMd=formSinais.cleaned_data['grupoCMe'])) &
                 (Q(cmE=formSinais.cleaned_data['cmE']) | Q(cmD=formSinais.cleaned_data['cmE']))
             ).distinct()

         elif localizacao == 0 and movimentacao == 0 and grupo != 0 and mao == 0:
             print('PASSEI grupo')
             return sinaisGlossario.filter(
                 (Q(grupoCMe=formSinais.cleaned_data['grupoCMe']) | Q(grupoCMd=formSinais.cleaned_data['grupoCMe']))
             ).distinct()

         elif localizacao == 0 and movimentacao == 0 and grupo != 0 and mao != 0:
             print('PASSEI  grupo + mao')
             return sinaisGlossario.filter(
                 (Q(grupoCMe=formSinais.cleaned_data['grupoCMe']) | Q(grupoCMd=formSinais.cleaned_data['grupoCMe'])) &
                 (Q(cmE=formSinais.cleaned_data['cmE']) | Q(cmD=formSinais.cleaned_data['cmE']))
             ).distinct()

         elif localizacao == 0 and movimentacao == 0 and grupo == 0 and mao != 0:
             print('PASSEI  mao')
             return sinaisGlossario.filter(
                 (Q(cmE=formSinais.cleaned_data['cmE']) | Q(cmD=formSinais.cleaned_data['cmE']))
             ).distinct()

         elif localizacao != 0 and movimentacao == 0 and grupo != 0 and mao == 0:
             print('PASSEI  loca + grupo')
             return sinaisGlossario.filter(
                 Q(localizacao=formSinais.cleaned_data['localizacao']) &
                 (Q(grupoCMe=formSinais.cleaned_data['grupoCMe']) | Q(grupoCMd=formSinais.cleaned_data['grupoCMe']))
             ).distinct()

         elif localizacao != 0 and movimentacao == 0 and grupo == 0 and mao != 0:
             print('PASSEI  loca + mao')
             return sinaisGlossario.filter(
                 Q(localizacao=formSinais.cleaned_data['localizacao']) &
                 (Q(cmE=formSinais.cleaned_data['cmE']) | Q(cmD=formSinais.cleaned_data['cmE']))
             ).distinct()

         elif localizacao != 0 and movimentacao == 0 and grupo != 0 and mao != 0:
             print('PASSEI  loca + grupo + mao')
             return sinaisGlossario.filter(
                 Q(localizacao=formSinais.cleaned_data['localizacao']) &
                 (Q(grupoCMe=formSinais.cleaned_data['grupoCMe']) | Q(grupoCMd=formSinais.cleaned_data['grupoCMe'])) &
                 (Q(cmE=formSinais.cleaned_data['cmE']) | Q(cmD=formSinais.cleaned_data['cmE']))
             ).distinct()

         elif localizacao != 0 and movimentacao != 0 and grupo == 0 and mao != 0:
             print('PASSEI  loca + movi + grupo')
             return sinaisGlossario.filter(
                 Q(localizacao=formSinais.cleaned_data['localizacao']) &
                 Q(movimentacao=formSinais.cleaned_data['movimentacao']) &
                 (Q(cmE=formSinais.cleaned_data['cmE']) | Q(cmD=formSinais.cleaned_data['cmE']))

             ).distinct()

         elif localizacao != 0 and movimentacao != 0 and grupo == 0 and mao != 0:
             print('PASSEI  loca + movi + mao')
             return sinaisGlossario.filter(
                 Q(movimentacao=formSinais.cleaned_data['movimentacao']) &
                 (Q(cmE=formSinais.cleaned_data['cmE']) | Q(cmD=formSinais.cleaned_data['cmE']))
             ).distinct()
     else:
         return sinaisGlossario.filter(
             Q(traducaoP__icontains=resultadoTraducao)
         ).distinct()

def filterSinaisIng(formSinais, sinaisGlossario, resultadoTraducao):

    if resultadoTraducao == []:
        return sinaisGlossario.filter(
            Q(localizacao=formSinais.cleaned_data['localizacao']) and
            Q(movimentacao=formSinais.cleaned_data['movimentacao']) and
            Q(grupoCMe=formSinais.cleaned_data['grupoCMe']) and
            Q(grupoCMd=formSinais.cleaned_data['grupoCMe']) and
            Q(cmE=formSinais.cleaned_data['cmE']) and
            Q(cmD=formSinais.cleaned_data['cmE'])
        ).distinct()

    else:
        return sinaisGlossario.filter(
            Q(traducaoI__icontains=resultadoTraducao)
        ).distinct()
# -----------------------------------------Registro de Usuario-------------------------------------------------------------------

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
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
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



# -------------------------------------------------------------------------------------------------------------------------