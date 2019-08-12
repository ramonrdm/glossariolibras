var iconSelectMao;
var selectedTextMao;

window.onload = function(){

    selectedTextMao = document.getElementById('id_cmE');
    document.getElementById('cmE-widget').addEventListener('changedmao', function(mao){
       selectedTextMao.value = iconSelectMao.getSelectedValue();
    });

    iconSelectMao = new iconSelectMao("cmE-widget",
        {'selectedIconWidth':75,
        'selectedIconHeight':75,
        'iconsWidth':75,
        'iconsHeight':75
        });

    var iconsMao = [];

    iconsMao.push({'iconFilePathMao':'/static/img/X.svg','iconValueMao':''});
    iconsMao.push({'iconFilePathMao':'/static/img/configuracoes_de_mao/100/100.png', 'iconValueMao':'100'});
    iconsMao.push({'iconFilePathMao':'/static/img/configuracoes_de_mao/10e/10e.png', 'iconValueMao':'10e'});
    iconsMao.push({'iconFilePathMao':'/static/img/configuracoes_de_mao/11e/11e.png', 'iconValueMao':'3'});
    iconsMao.push({'iconFilePathMao':'/static/img/configuracoes_de_mao/144/144.png', 'iconValueMao':'4'});
    iconsMao.push({'iconFilePathMao':'/static/img/configuracoes_de_mao/14c/14c.png', 'iconValueMao':'5'});
    iconsMao.push({'iconFilePathMao':'/static/img/configuracoes_de_mao/186/186.png', 'iconValueMao':'6'});
    iconsMao.push({'iconFilePathMao':'/static/img/configuracoes_de_mao/1a4/1a4.png', 'iconValueMao':'7'});
    iconsMao.push({'iconFilePathMao':'/static/img/configuracoes_de_mao/1ba/1ba.png', 'iconValueMao':'8'});
    iconsMao.push({'iconFilePathMao':'/static/img/configuracoes_de_mao/1cd/1cd.png', 'iconValueMao':'1cd'});
    iconsMao.push({'iconFilePathMao':'/static/img/configuracoes_de_mao/1f5/1f5.png', 'iconValueMao':'1f5'});

    iconSelectMao.refresh(iconsMao);

};


