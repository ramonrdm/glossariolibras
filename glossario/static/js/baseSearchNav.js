$(document).ready(function() {

	// INICIALIZA O IMAGEPICKER
	$('select').imagepicker({
		show_label: true
	});

	// ADICIONA CLASSE HOVERABLE AOS THUMBNAILS
	$('.thumbnail').addClass('hoverable');
	// $('.thumbnail').addClass('modal-trigger');
	// $('.thumbnail').attr('href', '#modal1');

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

	// function showAvatar(){
	// 	$(thumbnail_localizacao_ref.id).click(function() {
	// 		if(thumbnail_localizacao_ref.opened){
	// 			thumbnail_localizacao_ref.opened = false;
	// 			$('.map').hide();
	// 		} else {
	// 			thumbnail_localizacao_ref.opened = true;
	// 			$('.map').show();
	// 		}
	// 	});
	// }

	// for(let i = 0; i < thumbnail_refs.length; i++){	
	// 	$(thumbnail_refs[i].id).click(function() {
	// 		if(thumbnail_refs[i].opened){
	// 			thumbnail_refs[i].opened = false;
	// 			$(thumbnail_not_refs[i]).hide();
	// 			$(thumbnail_refs[i].id.split('.')[0] + 'li').click(function() {
	// 				$(this).parent().prepend($(thumbnail_refs[i].id.split('.')[0] + 'li:contains("Selecionar")'));
	// 				$(this).parent().prepend(this);
	// 			});
	// 		} else {	
	// 			thumbnail_refs[i].opened = true;
	// 			$(thumbnail_not_refs[i]).show();
	// 		}
	// 	});
	// }
	
	// // INICIALIZA A FUNÇÃO PARA MOSTRAR O AVATAR
	// showAvatar();

	// INICIALIZA O IMAGEMAPSTER
	$('#modeloImg').mapster( {
		fillColor: '000000',
		mapKey: 'data-key',
		singleSelect: true,
		scaleMap: true,
		isDeselectable: false,
		showToolTip: true,
		areas: [
			{
				key: "1",
				toolTip: "Cabeça",
			},
			{
				key: "2",
				toolTip: "Ombros"
			},
			{
				key: "3",
				toolTip: "Braços"
			},
			{
				key: "4",
				toolTip: "Nariz"
			},
			{
				key: "5",
				toolTip: "Bochechas"
			},
			{
				key: "6",
				toolTip: "Boca"
			},
			{
				key: "7",
				toolTip: "Tronco"
			},
			{
				key: "8",
				toolTip: "Espaço-neutro"
			},
			{
				key: "9",
				toolTip: "Olhos"
			},
			{
				key: "10",
				toolTip: "Orelhas"
			},
			{
				key: "11",
				toolTip: "Pescoço"
			},
			{
				key: "12",
				toolTip: "Queixo"
			},
			{
				key: "13",
				toolTip: "Testa"
			},
			{
				key: "14",
				toolTip: "Mãos"
			}
			
		]
	});

	// CENTRALIZA O AVATAR
	$('#modeloImg').parent().css({"margin":"0 auto"});

	// GERENCIA EVENTOS RELACIONADOS AO CLIQUE EM UMA ÁREA
	$('area').click(function() {

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

		$(document).css({'width':'100%'})
		$('.modal').modal();
		
	function bodyFix() {
	}


// RESPONSIVIDADE

// var resizeTime = 100;     // total duration of the resize effect, 0 is instant
// var resizeDelay = 100;    // time to wait before checking the window size again
//                           // the shorter the time, the more reactive it will be.

// // Resize the map to fit within the boundaries provided

// function resize(maxWidth,maxHeight) {
//      var image =  $('img'),
//         imgWidth = image.width(),
//         imgHeight = image.height(),
//         newWidth=0,
//         newHeight=0;

//     if (imgWidth/maxWidth>imgHeight/maxHeight) {
//         newWidth = maxWidth;
//     } else {
//         newHeight = maxHeight;
//     }
//     image.mapster('resize',newWidth,newHeight,resizeTime);   
// }

// // Track window resizing events, but only actually call the map resize when the
// // window isn't being resized any more

// function onWindowResize() {
    
//     var curWidth = $('.map').width(),
//         curHeight = $('.map').height(),
//         checking=false;
//     if (checking) {
//         return;
//             }
//     checking = true;
//     window.setTimeout(function() {
//         var newWidth = $('.map').width(),
//            newHeight = $('.map').height();
//         if (newWidth === curWidth &&
//             newHeight === curHeight) {
//             resize(newWidth,newHeight); 
//         }
//         checking=false;
//     },resizeDelay );
// }

// $(window).bind('resize',onWindowResize);

});