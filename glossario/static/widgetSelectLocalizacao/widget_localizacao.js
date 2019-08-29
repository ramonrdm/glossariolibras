$(document).ready(function(){
	//$("#imagem_localizacao").hide();
	$('.modal').modal();
	$('#modeloImg').parent().css({"margin":"0 auto"});




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
});