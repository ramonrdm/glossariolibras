$(document).ready(function() {

	// INICIALIZA O IMAGEPICKER
	$('select').imagepicker({
		show_label: true
	});

	// ADICIONA EFEITO DE HOVER AOS THUMBNAILS
	$('.thumbnail').addClass('hoverable');

	// USA SOMENTE CM E GRUPOCM ESQUERDA POIS TANTO FAZ PARA A PESQUISA
	let modal_refs = [
		'#modalGrupoCMe',
		'#modalCMe'
	];

	let select_refs = [
		'#id_grupoCMe',
		'#id_cmE'
	];

	// ATUALIZA THUMBNAIL EXIBIDO NA SIDENAV QUANDO ALGUM É SELECIONADO NO MODAL
	function sideNavThumbnailRefresh() {
		for(let i = 0; i < modal_refs.length; i++){
			$(modal_refs[i] + ' .thumbnail').click(function() {
				let attrValue = $(this).find('p').html();

				// REMOVE ATRIBUTO 'SELECTED' DA OPTION QUE JÁ ESTAVA SELECIONADA
				$(".formSinais select" + select_refs[i] + " option[selected='selected']").removeAttr('selected');

				let selectedOption = $(".formSinais select" + select_refs[i] + " option[value='" + attrValue + "']");

				// ADICIONA ATRIBUTO 'SELECTED' À OPTION CLICADA
				$(selectedOption).attr('selected', 'selected');

				// MOVE A OPTION SELECIONADA PARA O COMEÇO DO SELECT PARA NÃO SER DESLOCADA
				$(selectedOption).parent().prepend(selectedOption);

				// RECONSTRÓI O IMAGEPICKER PARA ATUALIZAR THUMBNAIL EXIBIDO
				$('select' + select_refs[i]).imagepicker({
					show_label: true
				});

				// ADICIONA EFEITO DE HOVER AOS THUMBNAILS NOVAMENTE APOS RECONSTRUÇÃO DO IMAGEPICKER
				$('.thumbnail').addClass('hoverable');

				// VINCULA A THUMBNAIL DA SIDENAV AO EVENTO DE CLIQUE NOVAMENTE
				sideNavThumbnailRefresh();
			});
		}
	}

	// INICIALIZA A FUNÇÃO PARA ATUALIZAR THUMBNAIL NA SIDENAV
	sideNavThumbnailRefresh();

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

		// VINCULA A ÁREA CLICADA À OPTION DA SUA LOCALIZAÇÃO
		let attrValue = $(this).attr('data-key');
		$("#id_localizacao option[selected='selected']").removeAttr('selected');
		$("#id_localizacao option[value='" + attrValue + "']").attr('selected', 'selected');

		// CORRIGE DESLOCAMENTO DO IMAGEPICKER
		$('#id_localizacao option').parent().prepend($('#id_localizacao option[selected="selected"]'));

		// RECONSTRÓI O IMAGEPICKER PARA ATUALIZAR THUMBNAIL EXIBIDO
		$('select#id_localizacao').imagepicker({
			show_label: true
		});

		// ADICIONA EFEITO DE HOVER AOS THUMBNAILS NOVAMENTE APOS RECONSTRUÇÃO DO IMAGEPICKER
		$('.thumbnail').addClass('hoverable');

	});

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