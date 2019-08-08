var iconSelectMao-100;
var selectedTextMao;

window.onload = function(){

    selectedTextMao = document.getElementById('id_cmE');
    document.getElementById('cmE-widget').addEventListener('changed', function(e){
       selectedTextMao.value = iconSelectMao.getSelectedValue();
    });

    iconSelectMao = new iconSelectMao-1("cmE-widget",
        {'selectedIconWidth':75,
        'selectedIconHeight':75,
        'iconsWidth':75,
        'iconsHeight':75
        });

    var iconsMao = [];

    iconsMao.push({'iconFilePath':'/static/img/X.svg','iconValue':''});
    iconsMao.push({'iconFilePath':'/static/img/configuracoes_de_mao/100/100.png', 'iconValue':'100'});
    iconsMao.push({'iconFilePath':'/static/img/configuracoes_de_mao/10e/10e.png', 'iconValue':'10e'});
    iconsMao.push({'iconFilePath':'/static/img/configuracoes_de_mao/11e/11e.png', 'iconValue':'11e'});
    iconsMao.push({'iconFilePath':'/static/img/configuracoes_de_mao/144/144.png', 'iconValue':'144'});
    iconsMao.push({'iconFilePath':'/static/img/configuracoes_de_mao/14c/14c.png', 'iconValue':'14c'});
    iconsMao.push({'iconFilePath':'/static/img/configuracoes_de_mao/186/186.png', 'iconValue':'186'});
    iconsMao.push({'iconFilePath':'/static/img/configuracoes_de_mao/1a4/1a4.png', 'iconValue':'1a4'});
    iconsMao.push({'iconFilePath':'/static/img/configuracoes_de_mao/1ba/1ba.png', 'iconValue':'1ba'});
    iconsMao.push({'iconFilePath':'/static/img/configuracoes_de_mao/1cd/1cd.png', 'iconValue':'1cd'});
    iconsMao.push({'iconFilePath':'/static/img/configuracoes_de_mao/1f5/1f5.png', 'iconValue':'1f5'});

    iconSelectMao.refresh(iconsMao);

};


