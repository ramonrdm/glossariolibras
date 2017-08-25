$(document).ready(function() {

$('select').imagepicker({
	show_label: true
});

//EXIBIR

$('#id_localizacao .selected').click(function() {
	$('#id_localizacao .thumbnail').show();
});	

//ESCONDER

$('#id_localizacao .thumbnail:not(.selected)').click(function() {
	$('#id_localizacao .thumbnail:not(.selected)').hide();
});

});