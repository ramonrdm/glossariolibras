# -*- coding: utf-8 -*-
from django.shortcuts import render
from glossario.models import Glossario, Sinal, Usuario, Tema
from glossario.forms import PesquisaForm
from django.http import JsonResponse
from django.db.models import Q
import json

def index(request, glossario=None):
	glossarios = Glossario.objects.all()
	return render(request, "index.html", {'glossarios': glossarios})

def glossarioSelecionado(request, glossario):
	try:
		glossario = Glossario.objects.get(link=glossario)
	except Glossario.DoesNotExist:
		glossario = None

	if request.method == 'POST':
		sinais = sinaisP = sinaisI = sinaisGlossario = formulario = None
		formulario = PesquisaForm(request.POST)
		checkboxPort = request.POST.get('checkboxPort', False)
		checkboxIng = request.POST.get('checkboxIng', False)

		# checkPort = request.session['checkboxPort']
		# checkIng = request.session['checkboxIng']

		sinaisGlossario = Sinal.objects.filter(glossario=glossario)
		if checkboxPort and checkboxIng:
			if formulario.is_valid():
				sinaisP = sinaisGlossario.filter(traducaoP__icontains=formulario.cleaned_data['busca'])
				sinaisI = sinaisGlossario.filter(traducaoI__icontains=formulario.cleaned_data['busca'])
		if checkboxPort and not checkboxIng:
			if formulario.is_valid():
				sinais = sinaisGlossario.filter(traducaoP__icontains=formulario.cleaned_data['busca'])
		if checkboxIng and not checkboxPort:
			if formulario.is_valid():
				sinais = sinaisGlossario.filter(traducaoI__icontains=formulario.cleaned_data['busca'])
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
			'formulario': formulario, 'sinais': sinais, 'sinaisP': sinaisP, 'sinaisI': sinaisI, 'sinaisGlossario': sinaisGlossario,
			'resultado': resultado, 'resultadoP': resultadoP, 'resultadoI': resultadoI, 'glossario': glossario,
			'checkboxPort': checkboxPort, 'checkboxIng': checkboxIng
			})
	else:
		formulario = PesquisaForm()
		return render(request, 'glossario.html', {'glossario': glossario, 'formulario': formulario})

def sinal(request, sinal=None, glossario=None):
	
	# request.session['checkboxPort'] = checkPort
	# request.session['checkboxIng'] = checkIng

	if sinal:
		try:
			sinal = Sinal.objects.get(id=sinal)
			glossario = sinal.glossario
		except Sinal.DoesNotExist:
			sinal = None

	if request.method == 'POST':
		sinais = sinaisP = sinaisI = sinaisGlossario = formulario = None
		formulario = PesquisaForm(request.POST)
		checkboxPort = request.POST.get('checkboxPort', False)
		checkboxIng = request.POST.get('checkboxIng', False)
		sinaisGlossario = Sinal.objects.filter(glossario=glossario)
		if checkboxPort and checkboxIng:
			if formulario.is_valid():
				sinaisP = sinaisGlossario.filter(traducaoP__icontains=formulario.cleaned_data['busca'])
				sinaisI = sinaisGlossario.filter(traducaoI__icontains=formulario.cleaned_data['busca'])
		if checkboxPort and not checkboxIng:
			if formulario.is_valid():
				sinais = sinaisGlossario.filter(traducaoP__icontains=formulario.cleaned_data['busca'])
		if checkboxIng and not checkboxPort:
			if formulario.is_valid():
				sinais = sinaisGlossario.filter(traducaoI__icontains=formulario.cleaned_data['busca'])
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
			'formulario': formulario, 'sinais': sinais, 'sinaisP': sinaisP, 'sinaisI': sinaisI, 'sinaisGlossario': sinaisGlossario,
			'resultado': resultado, 'resultadoP': resultadoP, 'resultadoI': resultadoI, 'glossario': glossario,
			'checkboxPort': checkboxPort, 'checkboxIng': checkboxIng
			})
	else:
		formulario = PesquisaForm()
		return render(request, "sinal.html", {'sinal': sinal, 'glossario': glossario, 'formulario': formulario})

def historia(request):
	return render(request, "historia.html")

def equipe(request):
	usuario = Usuario.objects.all()
	return render(request, "equipe.html", {'usuario': usuario})

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

#MÉTODO GENÉRICO PARA PESQUISA DE SINAIS - REUSABILIDADE DE CÓDIGO
#PROBLEMAS COM (request.POST) da PesquisaForm

# def pesquisaSinais():
# 		sinais = sinaisP = sinaisI = sinaisGlossario = formulario = None
# 		formulario = PesquisaForm(request.POST)
# 		checkboxPort = request.POST.get('checkboxPort', False)
# 		checkboxIng = request.POST.get('checkboxIng', False)
# 		sinaisGlossario = Sinal.objects.filter(glossario=glossario)
# 		if checkboxPort and checkboxIng:
# 			if formulario.is_valid():
# 				sinaisP = sinaisGlossario.filter(traducaoP__icontains=formulario.cleaned_data['busca'])
# 				sinaisI = sinaisGlossario.filter(traducaoI__icontains=formulario.cleaned_data['busca'])
# 		if checkboxPort and not checkboxIng:
# 			if formulario.is_valid():
# 				sinais = sinaisGlossario.filter(traducaoP__icontains=formulario.cleaned_data['busca'])
# 		if checkboxIng and not checkboxPort:
# 			if formulario.is_valid():
# 				sinais = sinaisGlossario.filter(traducaoI__icontains=formulario.cleaned_data['busca'])
# 		if sinais:
# 			resultado = len(sinais)
# 		else:
# 			resultado = None
# 		if sinaisP:
# 			resultadoP = len(sinaisP)
# 		else:
# 			resultadoP = None
# 		if sinaisI:
# 			resultadoI = len(sinaisI)
# 		else:
# 			resultadoI = None
# 		return render(request, 'pesquisa.html', {
# 			'formulario': formulario, 'sinais': sinais, 'sinaisP': sinaisP, 'sinaisI': sinaisI,
# 			'resultado': resultado, 'resultadoP': resultadoP, 'resultadoI': resultadoI, 'glossario': glossario,
# 			'checkboxPort': checkboxPort, 'checkboxIng': checkboxIng
# 			})