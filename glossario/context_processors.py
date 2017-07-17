def add_variable_to_context(request):
    return {
        'formulario': PesquisaForm(),
        # 'checkboxPortSession': request.session['checkboxPort'],
        # 'checkboxIngSession': request.session['checkboxIng']
    }