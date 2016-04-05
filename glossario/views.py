# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from glossario.models import Glossario, Sinal, Usuario
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

def temas(request):

	return render_to_response("temas.html")

def sinal(request, sinal=None):
	if sinal:
		try:
			sinal = Sinal.objects.get(id=sinal)
			
		except Sinal.DoesNotExist:
			sinal = None
			
		return render_to_response("sinal.html", dict(sinal=sinal))