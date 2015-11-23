from django.shortcuts import render_to_response
from glossario.models import Glossario, Sinal
from glossario.forms import PesquisaPortForm, PesquisaIngForm

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

def pesquisa(request, glossario=None, tipopesq=None, form=None):
	if glossario:
		try:
			glossario = Glossario.objects.get(link=glossario)
			if tipopesq	== "p":
				form = PesquisaPortForm
				return render_to_response("pesquisa.html", dict(glossario=glossario, form=form))
			elif tipopesq =="e":
				form = PesquisaIngForm
				return render_to_response("pesquisa.html", dict(glossario=glossario, form=form))
			elif tipopesq =="s":
				form = None
				return render_to_response("pesquisa.html", dict(glossario=glossario, form=form))
		except Glossario.DoesNotExist:
			glossarios = Glossario.objects.all()
	else:
		return render_to_response("pesquisa.html", dict(glossario=glossario, tipopesq=tipopesq))

	return render_to_response("pesquisa.html", dict(glossario=glossario, tipopesq=tipopesq))

def equipe(request):

	return render_to_response("equipe.html")

def contato(request):
	return render_to_response("contato.html")

def historia(request):
	
	return render_to_response("historia.html")
 