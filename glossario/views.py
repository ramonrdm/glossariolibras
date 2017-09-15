# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from glossario.models import Glossario, Sinal, Tema, GrupoCM
from django.contrib.auth.models import User
from glossario.forms import PesquisaForm, PesquisaCheckboxForm, EnviarSinaisForm, PesquisaSinaisForm
from django.http import JsonResponse
from django.db.models import Q
from django.template import RequestContext
import json
import datetime

##################### VIEWS #####################

def index(request, glossario=None):
	glossarios = Glossario.objects.all()
	return render(request, "index.html", {'glossarios': glossarios})

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
			'checkboxIng': checkboxIng, 'formCheckbox': formCheckbox, 'formSinais': formSinais
			})

def sinal(request, sinal=None, glossario=None):
	if sinal:
		try:
			sinal = Sinal.objects.get(id=sinal)
			glossario = sinal.glossario
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
			'formSinais': formSinais
			})
	else:
		formPesquisa = PesquisaForm()
		formCheckbox = PesquisaCheckboxForm(request.session['sinaisCheckboxes'])
		formSinais = PesquisaSinaisForm(request.session['sinaisCheckboxes'])
		return render(request, "sinal.html", {'sinal': sinal, 'glossario': glossario, 'formPesquisa': formPesquisa,
			'formCheckbox': formCheckbox, 'formSinais': formSinais
			})

def historia(request):
	return render(request, "historia.html")

def equipe(request):
	usuarios = User.objects.all()
	return render(request, "equipe.html", {'usuarios': usuarios})

def contato(request):
	return render(request, "contato.html")

def temas(request, temas=None):
	global queryTemas
	queryTemas = Tema.objects.all()
	try:
		raiz = criaNodo(queryTemas.get(temaPai=None))
		mostraNodo(raiz, 0)
	except Tema.DoesNotExist:
		raiz = None
	return render(request, "temas.html", dict(raiz=raiz))

def enviarSinais(request):
	if request.method == 'POST':
		form = EnviarSinaisForm(request.POST, request.FILES)
		toastSucesso = True
		try:
			if form.is_valid():
				dados = form.save(commit=False)
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
				form = EnviarSinaisForm()
				return render(request, 'enviarsinais.html', {'form': form, 'toastSucesso': toastSucesso})
		except ValueError:
			toastRepetido = True
			return render(request, 'enviarsinais.html', {'form': form, 'toastRepetido': toastRepetido})
	else:
		form = EnviarSinaisForm()
		return render(request, 'enviarsinais.html', {'form': form})

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
		print str(n) + txt +nodoTema1.nome
		filhos = nodoTema1.filhos
		for filho in filhos:
			mostraNodo(filho, n+1)
	else:
		print str(n) + txt +nodoTema1.nome

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
	print jsonTemas
	return JsonResponse(jsonTemas)

#################### MÉTODOS ####################

def filterSinaisPort(formSinais, sinaisGlossario, resultadoTraducao):
	return sinaisGlossario.filter(
		# grupoCMe e cmE estão repetidos pois o form pesquisa só por um grupoCM e CM
				Q(traducaoP__icontains=resultadoTraducao) |
				Q(localizacao=formSinais.cleaned_data['localizacao']) |
				Q(grupoCMe=formSinais.cleaned_data['grupoCMe']) |
				Q(grupoCMd=formSinais.cleaned_data['grupoCMe']) |
				Q(cmE=formSinais.cleaned_data['cmE']) |
				Q(cmD=formSinais.cleaned_data['cmE'])
			).distinct()

def filterSinaisIng(formSinais, sinaisGlossario, resultadoTraducao):
	return sinaisGlossario.filter(
		# grupoCMe e cmE estão repetidos pois o form pesquisa só por um grupoCM e CM
				Q(traducaoI__icontains=resultadoTraducao) |
				Q(localizacao=formSinais.cleaned_data['localizacao']) |
				Q(grupoCMe=formSinais.cleaned_data['grupoCMe']) |
				Q(grupoCMd=formSinais.cleaned_data['grupoCMe']) |
				Q(cmE=formSinais.cleaned_data['cmE']) |
				Q(cmD=formSinais.cleaned_data['cmE'])
			).distinct()