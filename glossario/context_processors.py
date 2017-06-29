def add_variable_to_context(request):
    return {
        'formulario': PesquisaForm(),
        # "request.session['checkboxPort']": checkboxPort,
        # "request.session['checkboxIng']": checkboxIng
    }