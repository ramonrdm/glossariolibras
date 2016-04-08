# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from glossario.models import Glossario, Sinal, Usuario, Tema
from glossario.forms import PesquisaPortForm, PesquisaIngForm
from django.template import RequestContext

def index(request, glossario=None):
	if glossario:
		try:
			glossario = Glossario.objects.get(link=glossario)
			return render_to_response("glossario.html", dict(glossario=glossario))
		except Glossario.DoesNotExist:
			glossarios = Glossario.objects.all()
	else:		
		glossarios = Glossario.objects.all()

	return render_to_response("index.html", dict(glossarios=glossarios, glossario=glossario))

def pesquisa(request, glossario=None, tipopesq=None):
	try:
		glossario = Glossario.objects.get(link=glossario)
	except Glossario.DoesNotExist:
		glossario = None
	if request.method == "POST":
			
		if tipopesq == "p":
			formulario = PesquisaPortForm(request.POST)
			if formulario.is_valid():
				sinais = Sinal.objects.filter(traducaoP__contains=formulario.cleaned_data['traducaoP'])
				resultado = len(sinais)
				return render_to_response(
					"pesquisa.html", 
					context_instance=RequestContext(
					request, 
					{ 'glossario':glossario, 'formulario':formulario, "sinais":sinais, 'resultado':resultado}
					))
				
		elif tipopesq == "e":
			formulario = PesquisaIngForm(request.POST)
			if formulario.is_valid():
				sinais = Sinal.objects.filter(traducaoI__contains=formulario.cleaned_data['traducaoI'])
				resultado = len(sinais)
				return render_to_response(
					"pesquisa.html", 
					context_instance=RequestContext(
					request, 
					{ 'glossario':glossario, 'formulario':formulario, "sinais":sinais, 'resultado':resultado}
					))

		elif tipopesq == "s":
				sinais = None
		
		else:
			sinais = None
	else:
		formulario = PesquisaPortForm()
		sinais = None
	return render_to_response(
		"pesquisa.html", 
		context_instance=RequestContext(
		request, 
		{ 'glossario':glossario, 'formulario':formulario}
		))

def equipe(request):
	usuario = Usuario.objects.all()
	return render_to_response("equipe.html", dict(usuario=usuario))

def contato(request):
	return render_to_response("contato.html")

def historia(request):
	return render_to_response("historia.html")

class NodoTema:
	def __init__(self, tema, filhos):
		self.tema = tema
		self.filhos = filhos
	def filhos(self):
		return self.filhos

def criaNodo(temaPai):
	filhosPai = queryTemas.filter(temaPai=temaPai)
	filhos2 = list()
	if filhosPai:
		for filho in filhosPai:
			filhos2.append(criaNodo(filho))
	no = NodoTema(temaPai, filhos2)
	return no

def mostraNodo(nodoTema1, n):
	txt = " - "*n
	if nodoTema1.filhos:
		print str(n) + txt +nodoTema1.tema.nome
		filhos = nodoTema1.filhos
		for filho in filhos:
			mostraNodo(filho, n+1)
	else:
		print str(n) + txt +nodoTema1.tema.nome

def temas(request, temas=None):
	global queryTemas
	try:
		queryTemas = Tema.objects.all()
	except Tema.DoesNotExist:
		queryTemas = None

		return render_to_response("index.html")
	
	raiz = criaNodo(queryTemas.get(id=1))
	mostraNodo(raiz, 0)


	return render_to_response("temas.html", dict(raiz=raiz))

def sinal(request, sinal=None):
	if sinal:
		try:
			sinal = Sinal.objects.get(id=sinal)
			
		except Sinal.DoesNotExist:
			sinal = None
			
		return render_to_response("sinal.html", dict(sinal=sinal))