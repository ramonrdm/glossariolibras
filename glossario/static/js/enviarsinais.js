function inicia(){

    // INICIALIZA O IMAGEPICKER
    $('select').imagepicker({
        show_label: true
    });
    $('#id_grupoCMe').hide();

    // ADICIONA CLASSE HOVERABLE AOS THUMBNAILS
    $('.thumbnail').addClass('hoverable');

    // HIDE/SHOW IMAGEPICKER E AVATAR

    let thumbnail_refs = [
        {id: '#id_grupoCMe .thumbnail', opened: false},
        {id: '#id_grupoCMd .thumbnail', opened: false},
        {id: '#id_cmE .thumbnail', opened: false},
        {id: '#id_cmD .thumbnail', opened:false},
        {id: '#id_movimentacao .thumbnail', opened:false}
    ];

    let thumbnail_not_refs = [
        '#id_grupoCMe .thumbnail:not(.selected)',
        '#id_grupoCMd .thumbnail:not(.selected)',
        '#id_cmE .thumbnail:not(.selected)',
        '#id_cmD .thumbnail:not(.selected)',
        '#id_movimentacao .thumbnail:not(.selected)'
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
}




$(document).ready(function() {
    inicia();

});
