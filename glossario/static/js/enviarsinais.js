$(document).ready(function() {

	// INICIALIZA O IMAGEPICKER
	$('select').imagepicker({
		show_label: true
	});

	// ADICIONA CLASSE HOVERABLE AOS THUMBNAILS
	$('.thumbnail').addClass('hoverable');

	// HIDE/SHOW IMAGEPICKER E AVATAR

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
			if(thumbnail_refs[i].id === '#id_localizacao .thumbnail'){
				if(thumbnail_refs[i].opened){
					thumbnail_refs[i].opened = false;
					$('.map').hide();
				} else {
					thumbnail_refs[i].opened = true;
					$('.map').show();
				}
			}
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

	// INICIALIZA O IMAGEMAPSTER
	$('#modeloImg').mapster( {
		fillColor: '003a99',
		singleSelect: true,
		mapKey: 'data-key'
	});

	// VINCULA A ÁREA CLICADA À OPTION DA SUA LOCALIZAÇÃO E ESCONDE O AVATAR
	$('area').click(function() {
		$(this).mapster('set',true);
		thumbnail_refs[0].opened = false;
		$('.map').hide();
		let attrValue = $(this).attr('data-key');
		$("#id_localizacao option[selected='selected']").attr('selected', '');
		$("#id_localizacao option[value='" + attrValue + "']").attr('selected', 'selected');
	});

});