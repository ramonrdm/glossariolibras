def add_variable_to_context(request):
	return {
	'formulario': PesquisaForm(),
	'formCheckbox': PesquisaCheckboxForm(),
	# 'formCheckboxIng': PesquisaCheckboxForm()
	# 'request.POST': request.POST
	}