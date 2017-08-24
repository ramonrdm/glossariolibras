$(document).ready(function() {
$('select').imagepicker({
	show_label: true
});

//EXIBIR

// $('#id_localizacao').find('li div.thumbnail.selected').click(function() {
// 	$('#id_localizacao').find('li div.thumbnail').show();
// });
$('#id_localizacao li div.thumbnail.selected').click(function() {
	$('#id_localizacao li div.thumbnail').show();
});
$('#id_grupoCMe').find('li div.thumbnail.selected').click(function() {
	$('#id_grupoCMe').find('li div.thumbnail').show();
});
$('#id_grupoCMd').find('li div.thumbnail.selected').click(function() {
	$('#id_grupoCMd').find('li div.thumbnail').show();
});
$('#id_cmE').find('li div.thumbnail.selected').click(function() {
	$('#id_cmE').find('li div.thumbnail').show();
});
$('#id_cmD').find('li div.thumbnail.selected').click(function() {
	$('#id_cmD').find('li div.thumbnail').show();
});			

//ESCONDER

$('#id_localizacao').find('li div.thumbnail:not(.selected)').click(function() {
	$('#id_localizacao').find('li div.thumbnail:not(.selected)').hide();
	$('#id_localizacao').find('li div.thumbnail.selected').click(function(){
		$('#id_localizacao li div.thumbnail').show();
		}
		);
	

});
$('#id_grupoCMe').find('li div.thumbnail:not(.selected)').click(function() {
	$('#id_grupoCMe').find('li div.thumbnail:not(.selected)').hide();
});
$('#id_grupoCMd').find('li div.thumbnail:not(.selected)').click(function() {
	$('#id_grupoCMd').find('li div.thumbnail:not(.selected)').hide();
});
$('#id_cmE').find('li div.thumbnail:not(.selected)').click(function() {
	$('#id_cmE').find('li div.thumbnail:not(.selected)').hide();
});
$('#id_cmD').find('li div.thumbnail:not(.selected)').click(function() {
	$('#id_cmD').find('li div.thumbnail:not(.selected)').hide();
});
// $('div.thumbnail:not(.selected)').click(function() {
// 	$('div.thumbnail:not(.selected)').hide();
// });
});