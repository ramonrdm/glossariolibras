var iconSelect;

window.onload = function(){

    iconSelect = new IconSelect("movimentacao-widget",
        {'selectedIconWidth':100,
        'selectedIconHeight':100,
        'selectedBoxPadding':5,
        'iconsWidth':50,
        'iconsHeight':50,
        'boxIconSpace':2,
        'vectoralIconNumber':1,
        'horizontalIconNumber':2});

    var icons = [];

    icons.push({'iconFilePath':'/static/img/X.svg', 'valur':'0'});
    icons.push({'iconFilePath':'/static/img/parede.png', 'iconValue':'1'});
    icons.push({'iconFilePath':'/static/img/chao.png', 'iconValue':'2'});
    icons.push({'iconFilePath':'/static/img/circular.png', 'iconValue':'3'});
    icons.push({'iconFilePath':'/static/img/contato.png', 'iconValue':'4'});

    iconSelect.refresh(icons);

};