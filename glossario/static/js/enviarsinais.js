$(document).ready(function() {

	// INICIALIZA O IMAGEPICKER
	$('select').imagepicker({
		show_label: true
	});

	// ADICIONA CLASSE HOVERABLE AOS THUMBNAILS
	$('.thumbnail').addClass('hoverable');

	// HIDE/SHOW IMAGEPICKER E AVATAR

	let thumbnail_refs = [
		{id: '#id_grupoCMe .thumbnail', opened: false},
		{id: '#id_grupoCMd .thumbnail', opened: false},
		{id: '#id_cmE .thumbnail', opened: false},
		{id: '#id_cmD .thumbnail', opened:false}
	];

	let thumbnail_not_refs = [
		'#id_grupoCMe .thumbnail:not(.selected)',
		'#id_grupoCMd .thumbnail:not(.selected)',
		'#id_cmE .thumbnail:not(.selected)',
		'#id_cmD .thumbnail:not(.selected)'
	];

	let thumbnail_localizacao_ref = {id: '#id_localizacao .thumbnail', opened: false};

	function showAvatar(){
		$(thumbnail_localizacao_ref.id).click(function() {
			if(thumbnail_localizacao_ref.opened){
				thumbnail_localizacao_ref.opened = false;
				$('.map').hide();
			} else {
				thumbnail_localizacao_ref.opened = true;
				$('.map').show();
			}
		});
	}

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
	
	// INICIALIZA A FUNÇÃO PARA MOSTRAR O AVATAR
	showAvatar();

	// INICIALIZA O IMAGEMAPSTER
	$('#modeloImg').mapster( {
		fillColor: '003a99',
		mapKey: 'data-key',
		singleSelect: true,
		scaleMap: true,
		tooltip: true
	});

	// GERENCIA EVENTOS RELACIONADOS AO CLIQUE EM UMA ÁREA
	$('area').click(function() {

		// ÁREA NUNCA DEIXA DE SER SELECIONADA
		$(this).mapster('set',true);

		// ESCONDE O AVATAR
		thumbnail_localizacao_ref.opened = false;
		$('.map').hide();

		// VINCULA A ÁREA CLICADA À OPTION DA SUA LOCALIZAÇÃO
		let attrValue = $(this).attr('data-key');
		$("#id_localizacao option[selected='selected']").removeAttr('selected');
		$("#id_localizacao option[value='" + attrValue + "']").attr('selected', 'selected');

		// CORRIGE DESLOCAMENTO DO IMAGEPICKER
		$('#id_localizacao option').parent().prepend($('#id_localizacao option[selected="selected"]'));

		// RECONSTRÓI O IMAGEPICKER
		$('select#id_localizacao').imagepicker({
			show_label: true
		});
		$('.thumbnail').addClass('hoverable');

		// VINCULA O IMAGEPICKER AO EVENTO DE MOSTRAR O AVATAR NOVAMENTE
		showAvatar();

	});

});