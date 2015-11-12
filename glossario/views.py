from django.shortcuts import render_to_response
from glossario.models import Glossario

# Create your views here.

def index(request, glossario=None):
	if glossario:
		try:
			glossario = Glossario.objects.get(link=glossario)
		except Glossario.DoesNotExist:
			glossarios = Glossario.objects.all()

	else:		
		glossarios = Glossario.objects.all()

	return render_to_response("index.html", dict(glossarios=glossarios))