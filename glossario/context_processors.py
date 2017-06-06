def add_variable_to_context(request):
    return {
        'formulario': PesquisaForm()
        # 'glossario': Glossario.objects.get(link=glossario)
        # 'sinal': Sinal.objects.get(id=sinal)
    }