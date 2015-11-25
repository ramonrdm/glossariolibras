# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from glossario.models import Glossario, Sinal
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
	#tens que resolver as coisas por partes...

	#Verificar se tem um glossário especifico senao transforma ele em None
	try:
		glossario = Glossario.objects.get(link=glossario)
	except Glossario.DoesNotExist:
		glossario = None
	if request.method == "POST":
		formulario = PesquisaPortForm(request.POST)
		if formulario.is_valid():
			
			if tipopesq == "p":
				sinais = Sinal.objects.filter(traducaoP__contains=formulario.cleaned_data['traducaoP'])
				print sinais
				return render_to_response(
					"pesquisa.html", 
					context_instance=RequestContext(
					request, 
					{ 'glossario':glossario, 'formulario':formulario, "sinais":sinais, }
					))
				
			elif tipopesq == "e":
				sinais = None
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
		{ 'glossario':glossario, 'formulario':formulario, "sinais":sinais}
		))

def equipe(request):

	return render_to_response("equipe.html")

def contato(request):
	return render_to_response("contato.html")

def historia(request):
	
	return render_to_response("historia.html")
 