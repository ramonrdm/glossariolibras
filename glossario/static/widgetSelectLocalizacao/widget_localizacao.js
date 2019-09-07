$(document).ready(function(){
    //$("#imagem_localizacao").hide();

    $('.modal').modal();
    $('#modeloImg').parent().css({"margin":"0 auto"});
//      $('#modeloImg').mapster('resize',width,height,duration);

    $('#modeloImg').mapster( {
        fillColor: '000000',
        mapKey: 'data-key',
        singleSelect: true,
        scaleMap: true,
        isDeselectable: false,
        showToolTip: true,
        areas: [
            {
                key: "4",
                toolTip: "Cabeça",
            },
            {
                key: "12",
                toolTip: "Ombros"
            },
            {
                key: "3",
                toolTip: "Braços"
            },
            {
                key: "6",
                toolTip: "Nariz"
            },
            {
                key: "2",
                toolTip: "Bochechas"
            },
            {
                key: "1",
                toolTip: "Boca"
            },
            {
                key: "16",
                toolTip: "Tronco"
            },
            {
                key: "10",
                toolTip: "Espaço-neutro"
            },
            {
                key: "11",
                toolTip: "Olhos"
            },
            {
                key: "17",
                toolTip: "Orelhas"
            },
            {
                key: "13",
                toolTip: "Pescoço"
            },
            {
                key: "14",
                toolTip: "Queixo"
            },
            {
                key: "15",
                toolTip: "Testa"
            },
            {
                key: "5",
                toolTip: "Mãos"
            }

        ]
});
$('#modeloImg').parent().css({"margin":"0 auto"});

$('area').click(function() {
    let attrValue = $(this).attr('data-key');
    if(attrValue){
        $('#id_localizacao').val(attrValue);
        $('#imagem_localizacao').attr('src', '/static/img/'+objetos_localizacao[attrValue]);
        $('#imagem_localizacao_mobile').attr('src', '/static/img/'+objetos_localizacao[attrValue]);
    }else{
        $('#id_localizacao').val('');
        $('#imagem_localizacao').attr('src', '/static/img/X.svg');
        $('#imagem_localizacao_mobile').attr('src', '/static/img/X.svg');
    }
    

});

});
