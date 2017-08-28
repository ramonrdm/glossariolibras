$(document).ready(function() {

	// INICIALIZA O IMAGEPICKER
	$('select').imagepicker({
		show_label: true
	});

	// ADICIONA CLASSE HOVERABLE
	$('.thumbnail').addClass('hoverable');

	// var original = $(thumbnail_refs[i] + ' p:first');

	// HIDE/SHOW IMAGEPICKER

	let thumbnail_refs = [
		{id: '#id_localizacao .thumbnail', opened: false},
		{id: '#id_grupoCMe .thumbnail', opened: false},
		{id: '#id_grupoCMd .thumbnail', opened: false},
		{id: '#id_cmE .thumbnail', opened: false},
		{id: '#id_cmD .thumbnail', opened:false}
	];

	let thumbnail_not_refs = [
		'#id_localizacao .thumbnail:not(.selected)',
		'#id_grupoCMe .thumbnail:not(.selected)',
		'#id_grupoCMd .thumbnail:not(.selected)',
		'#id_cmE .thumbnail:not(.selected)',
		'#id_cmD .thumbnail:not(.selected)'
	];

	for(let i = 0; i < thumbnail_refs.length; i++){	
		$(thumbnail_refs[i].id).click(function() {
			if(thumbnail_refs[i].opened){
				thumbnail_refs[i].opened = false;
				$(thumbnail_not_refs[i]).hide();
				$(thumbnail_refs[i].id.split('.')[0] + 'li').click(function() {
					$(this).parent().prepend($(thumbnail_refs[i].id.split('.')[0] + 'li:contains("Selecionar")'));
					$(this).parent().prepend(this);
				});
			} else {	
				thumbnail_refs[i].opened = true;
				$(thumbnail_not_refs[i]).show();
			}
		});
	}

});