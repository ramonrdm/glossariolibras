var iconSelectMao;
var selectedTextMao;

window.onload = function(){

    selectedTextMao = document.getElementById('id_cmE');
    document.getElementById('cmE-widget').addEventListener('changed', function(e){
       selectedTextMao.value = iconSelectMao.getSelectedValue();
    });

    iconSelectMao = new iconSelectMao("cmE-widget",
        {'selectedIconWidth':85,
        'selectedIconHeight':85,
        'iconsWidth':85,
        'iconsHeight':85
        });

    var iconsMao = [];

    iconsMao.push({'iconFilePath':'/static/img/X.svg', 'iconValue':'0'});
    iconsMao.push({'iconFilePath':'/static/img/configuracoes_de_mao/1a4/1a4.png', 'iconValue':'1'});
    iconsMao.push({'iconFilePath':'/static/img/configuracoes_de_mao/1ba/1ba.png', 'iconValue':'2'});
    iconsMao.push({'iconFilePath':'/static/img/configuracoes_de_mao/1cd/1cd.png', 'iconValue':'3'});
    iconsMao.push({'iconFilePath':'/static/img/configuracoes_de_mao/1f5/1f5.png', 'iconValue':'4'});
    iconsMao.push({'iconFilePath':'/static/img/configuracoes_de_mao/10e/10e.png', 'iconValue':'5'});
    iconsMao.push({'iconFilePath':'/static/img/configuracoes_de_mao/11e/11e.png', 'iconValue':'6'});
    iconsMao.push({'iconFilePath':'/static/img/configuracoes_de_mao/14c/14c.png', 'iconValue':'7'});
    iconsMao.push({'iconFilePath':'/static/img/configuracoes_de_mao/100/100.png', 'iconValue':'8'});
    iconsMao.push({'iconFilePath':'/static/img/configuracoes_de_mao/144/144.png', 'iconValue':'9'});
    iconsMao.push({'iconFilePath':'/static/img/configuracoes_de_mao/186/186.png', 'iconValue':'10'});


    iconSelectMao.refresh(iconsMao);




    var _1a4 = [];

    _1a4.push({'iconFilePath':'/static/img/X.svg', 'iconValue':'0'});
    _1a4.push({'iconFilePath':'/static/img/configuracoes_de_mao/1a4/1a4.png', 'iconValue':'1'});
    _1a4.push({'iconFilePath':'/static/img/configuracoes_de_mao/1ba/1ba.png', 'iconValue':'2'});
    _1a4.push({'iconFilePath':'/static/img/configuracoes_de_mao/1cd/1cd.png', 'iconValue':'3'});
    _1a4.push({'iconFilePath':'/static/img/configuracoes_de_mao/1f5/1f5.png', 'iconValue':'4'});
    _1a4.push({'iconFilePath':'/static/img/configuracoes_de_mao/10e/10e.png', 'iconValue':'5'});
    _1a4.push({'iconFilePath':'/static/img/configuracoes_de_mao/11e/11e.png', 'iconValue':'6'});
    _1a4.push({'iconFilePath':'/static/img/configuracoes_de_mao/14c/14c.png', 'iconValue':'7'});
    _1a4.push({'iconFilePath':'/static/img/configuracoes_de_mao/100/100.png', 'iconValue':'8'});
    _1a4.push({'iconFilePath':'/static/img/configuracoes_de_mao/144/144.png', 'iconValue':'9'});
    _1a4.push({'iconFilePath':'/static/img/configuracoes_de_mao/186/186.png', 'iconValue':'10'});


    iconSelectMao.refresh(_1a4);

};