# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from glossario.models import Glossario, Sinal, Usuario, Tema
from glossario.forms import PesquisaPortForm, PesquisaIngForm, PesquisaForm
from django.template import RequestContext
from django.http import JsonResponse
from django.db.models import Q
import json

def index(request, glossario=None):
	# if glossario:
	# 	try:
	# 		#glossario = Glossario.objects.get(link=glossario)
	# 		#return render(request, "glossario.html", dict(glossario=glossario))
	# 		return redirect('viewGlossario')
	# 	except Glossario.DoesNotExist:
	# 		glossarios = Glossario.objects.all()
	# else:

	# if glossario:
	# 	try:
	# 		return redirect('glossarioSelecionado')
	# 	except Glossario.DoesNotExist:
	# 		glossarios = Glossario.objects.all()

	glossarios = Glossario.objects.all()
	return render(request, "index.html", {'glossarios': glossarios})

def glossarioSelecionado(request, glossario): #LÓGICA DAS CHECKBOXES IMPLEMENTADAS SOMENTE PARA ESTA VIEW, FAZER PARA AS OUTRAS
	try:
		glossario = Glossario.objects.get(link=glossario)
	except Glossario.DoesNotExist:
		glossario = None

	if request.method == 'POST':
		sinais = sinaisP = sinaisI = formulario = None
		formulario = PesquisaForm(request.POST)
		checkboxPort = request.POST.get('checkboxPort', False)
		checkboxIng = request.POST.get('checkboxIng', False)
		if checkboxPort and checkboxIng:
			if formulario.is_valid():
				sinaisP = Sinal.objects.filter(traducaoP__icontains=formulario.cleaned_data['busca'])
				sinaisI = Sinal.objects.filter(traducaoI__icontains=formulario.cleaned_data['busca'])
		if checkboxPort and not checkboxIng:
			if formulario.is_valid():
				sinais = Sinal.objects.filter(traducaoP__icontains=formulario.cleaned_data['busca'])
		if checkboxIng and not checkboxPort:
			if formulario.is_valid():
				sinais = Sinal.objects.filter(traducaoI__icontains=formulario.cleaned_data['busca'])
		if sinais:
			resultado = len(sinais)
		else:
			resultado = None
		if sinaisP:
			resultadoP = len(sinaisP)
		else:
			resultadoP = None
		if sinaisI:
			resultadoI = len(sinaisI)
		else:
			resultadoI = None
		return render(request, 'pesquisa.html', {
			'formulario': formulario, 'sinais': sinais, 'sinaisP': sinaisP, 'sinaisI': sinaisI,
			'resultado': resultado, 'resultadoP': resultadoP, 'resultadoI': resultadoI, 'glossario': glossario,
			'checkboxPort': checkboxPort, 'checkboxIng': checkboxIng
			})
	else:
		formulario = PesquisaForm()
		return render(request, 'glossario.html', {'glossario': glossario, 'formulario': formulario})

def pesquisa(request, glossario=None, tipopesq=None, formulario=None, sinais=None, resultado=None):
	if request.method == 'POST':
		sinais = formulario = None
		formulario = PesquisaForm(request.POST)
		if formulario.is_valid():
			sinais = Sinal.objects.filter(Q(traducaoP__icontains=formulario.cleaned_data['busca']) | Q(traducaoI__icontains=formulario.cleaned_data['busca']))
		if(sinais):
			resultado = len(sinais)
		else:
			resultado = None
		return render(request, 'pesquisa.html', {'formulario': formulario, 'sinais': sinais, 'resultado': resultado, 'glossario': glossario})
	else:
		formulario = PesquisaForm()
		return render(request, 'pesquisa.html', {'formulario': formulario, 'sinais': sinais, 'resultado': resultado, 'glossario': glossario})

	# if request.method == "POST":
	# 	if tipopesq == "p":
	# 		formulario = PesquisaPortForm(request.POST, auto_id=False)
	# 		if formulario.is_valid():
	# 			sinais = Sinal.objects.filter(traducaoP__contains=formulario.cleaned_data['traducaoP'])		
	# 	elif tipopesq == "e":
	# 		formulario = PesquisaIngForm(request.POST, auto_id=False)
	# 		if formulario.is_valid():
	# 			sinais = Sinal.objects.filter(traducaoI__contains=formulario.cleaned_data['traducaoI'])
	# 	elif tipopesq == "s":
	# 		#pesquisa pelo parametros do Libras, local, grupoCM, CMs
	# 		sinais = None
	# else:
	# 	if tipopesq == "p":
	# 		formulario = PesquisaPortForm(auto_id=False)
	# 	elif tipopesq == "e":
	# 		formulario = PesquisaIngForm(auto_id=False)
	# 	elif tipopesq == "s":
	# 		#pesquisa pelo parametros do Libras, local, grupoCM, CMs 

	#return render(request, "pesquisa.html", {'glossario':glossario,'formulario':formulario,'sinais':sinais,'nsinais':resultado,'tipopesq':tipopesq})


def equipe(request):
	usuario = Usuario.objects.all()
	return render(request, "equipe.html", {'usuario': usuario})

def contato(request):
	return render(request, "contato.html")

def historia(request):
	return render(request, "historia.html")

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

def temas(request, temas=None):
	global queryTemas
	queryTemas = Tema.objects.all()
	try:
		raiz = criaNodo(queryTemas.get(id=1))
		mostraNodo(raiz, 0)
	except Tema.DoesNotExist:
		raiz = None
	return render(request, "temas.html", dict(raiz=raiz))

def sinal(request, sinal=None, glossario=None):
	if sinal:
		try:
			sinal = Sinal.objects.get(id=sinal)
			glossario = sinal.glossario
		except Sinal.DoesNotExist:
			sinal = None

	if request.method == 'POST':
		sinais = formulario = None
		formulario = PesquisaForm(request.POST)
		if formulario.is_valid():
			sinais = Sinal.objects.filter(Q(traducaoP__icontains=formulario.cleaned_data['busca']) | Q(traducaoI__icontains=formulario.cleaned_data['busca']))
		if(sinais):
			resultado = len(sinais)
		else:
			resultado = None
		return render(request, 'pesquisa.html', {'formulario': formulario, 'sinais': sinais, 'resultado': resultado, 'glossario': glossario})
	else:
		formulario = PesquisaForm()
		return render(request, "sinal.html", {'sinal': sinal, 'glossario': glossario, 'formulario': formulario})

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
	raiz = criaNodo(Tema.objects.get(id=1))
	mostraNodoJson(raiz)
	print jsonTemas
	return JsonResponse(jsonTemas)