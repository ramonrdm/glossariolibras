$(document).ready(function () {    
    $('.modal').modal();
    var valor_localizacao = JSON.parse(document.getElementById('valor_localizacao').textContent);
    var objetos_localizacao = JSON.parse(document.getElementById('objetos_localizacao').textContent);
    // Trata a escolha na versão mobile
    if(valor_localizacao){
        $('#imagem_localizacao').attr('src', '/static/img/' + objetos_localizacao[valor_localizacao]);
        // Se for escolhido sem localização, então ignora a localização dos sinais na busca
        if (valor_localizacao != 0) {
            $('#id_localizacao').val(valor_localizacao);
        } else {
            $('#id_localizacao').val('');
        }
    }
        
    $('.escolhaLocalizacao').click(function(){
        var escolhaLocalizacao = $(this).children('img').attr('id-field');
        $('#imagem_localizacao').attr('src', $(this).children('img').attr('src'));
        if (escolhaLocalizacao != 0) {
            $('#id_localizacao').val(escolhaLocalizacao);
        } else {
            $('#id_localizacao').val('');
        }
    });

    // Trata a escolha na versão Desktop
    $('#modeloImg').mapster({
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
            },
            {
                key: "0",
                toolTip: "Sem Localização"
            }

        ]
    });
    $('#modeloImg').parent().css({ "margin": "0 auto" });

    $('area').click(function () {
        let attrValue = $(this).attr('data-key');
        if (attrValue) {
            $('#imagem_localizacao').attr('src', '/static/img/' + objetos_localizacao[attrValue]);
            if (attrValue != 0) {
                $('#id_localizacao').val(attrValue);
            } else {
                $('#id_localizacao').val('');
            }
        } else {
            $('#id_localizacao').val('');
            $('#imagem_localizacao').attr('src', '/static/img/L.jpg');
        }
    });
});
