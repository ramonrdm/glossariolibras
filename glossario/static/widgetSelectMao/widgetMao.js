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

    var icons = [];

    icons.push({'iconFilePath':'/static/img/X.svg', 'iconValue':'0'});
    icons.push({'iconFilePath':'/static/img/parede.png', 'iconValue':'1'});
    icons.push({'iconFilePath':'/static/img/chao.png', 'iconValue':'2'});
    icons.push({'iconFilePath':'/static/img/circular.png', 'iconValue':'3'});
    icons.push({'iconFilePath':'/static/img/contato.png', 'iconValue':'4'});

    iconSelectMao.refresh(icons);

};