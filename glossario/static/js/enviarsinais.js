$(document).ready(function() {

	$('select').imagepicker({
		show_label: true
	});

	$('.thumbnail').addClass('hoverable');

	// HIDE/SHOW DO IMAGEPICKER

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
			} else {	
				thumbnail_refs[i].opened = true;
				$(thumbnail_not_refs[i]).show();
			}
		});
	}

});