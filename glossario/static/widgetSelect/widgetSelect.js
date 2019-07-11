var iconSelect;
var selectedText;

window.onload = function(){

    selectedText = document.getElementById('selected-text');
    document.getElementById('my-icon-select').addEventListener('changed', function(e){
       selectedText.value = iconSelect.getSelectedValue();
    });

    iconSelect = new IconSelect("movimentacao-widget",
        {'selectedIconWidth':90,
        'selectedIconHeight':90,
        'selectedBoxPadding':0,
        'iconsWidth':50,
        'iconsHeight':50,
        'boxIconSpace':0,
        'vectoralIconNumber':1,
        'horizontalIconNumber':2});

    var icons = [];

    icons.push({'iconFilePath':'/static/img/X.svg', 'iconValue':'0'});
    icons.push({'iconFilePath':'/static/img/parede.png', 'iconValue':'1'});
    icons.push({'iconFilePath':'/static/img/chao.png', 'iconValue':'2'});
    icons.push({'iconFilePath':'/static/img/circular.png', 'iconValue':'3'});
    icons.push({'iconFilePath':'/static/img/contato.png', 'iconValue':'4'});

    iconSelect.refresh(icons);

};