from django.shortcuts import render_to_response, render
from glossario.models import Glossario, Sinal
from glossario.forms import PesquisaPortForm, PesquisaIngForm
from django.template import RequestContext
# Create your views here.

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
	if glossario:
		try:	
			glossario = Glossario.objects.get(link=glossario)
			if tipopesq	== "p":
				if request.method == "POST":
					formulario = PesquisaPortForm()
					request.POST = request.POST.copy()
					return render_to_response("pesquisa.html", dict(glossario=glossario, formulario=formulario, context_instance=RequestContext(request)))
				else:
					formulario = PesquisaPortForm()
					return render_to_response("pesquisa.html", dict(glossario=glossario, formulario=formulario, context_instance=RequestContext(request)))

			elif tipopesq =="e":
				formulario = PesquisaIngForm()
				if request.method == "POST":
					return render_to_response("pesquisa.html", dict(glossario=glossario, formulario=formulario, context_instance=RequestContext(request)))
				return render_to_response("pesquisa.html", dict(glossario=glossario, formulario=formulario, context_instance=RequestContext(request)))

			elif tipopesq =="s":
				formulario = None
				if request.method == "POST":
					return render_to_response("pesquisa.html", dict(glossario=glossario, formulario=formulario, context_instance=RequestContext(request)))
				return render_to_response("pesquisa.html", dict(glossario=glossario, formulario=formulario, context_instance=RequestContext(request)))
					
		except Glossario.DoesNotExist:
			glossarios = Glossario.objects.all()
			return render_to_response("index.html", dict(glossarios=glossarios, glossario=glossario))
	else:
		return render_to_response("index.html", dict(glossarios=glossarios, glossario=glossario))

def equipe(request):

	return render_to_response("equipe.html")

def contato(request):
	return render_to_response("contato.html")

def historia(request):
	
	return render_to_response("historia.html")
 