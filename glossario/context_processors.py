def add_variable_to_context(request):
	return {
	'formulario': PesquisaForm(),
	'formCheckbox': PesquisaCheckboxForm(),
	'checkboxPortSession': request.session['checkboxPort'],
	'checkboxIngSession': request.session['checkboxIng']
	}