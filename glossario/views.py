from django.shortcuts import render_to_response
from glossario.models import Glossario

# Create your views here.

def index(request):
	glossarios = Glossario.objects.all()

	return render_to_response("index.html", dict(glossarios=glossarios))