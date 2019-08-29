var iconSelect;
var selectedText;

window.onload = function(){

    selectedText = document.getElementById('id_cmE');
    console.log(selectedText.innerHtml);
    document.getElementById('cmE-widget').addEventListener('changed', function(e){
       selectedText.value = iconSelect.getSelectedValue();
    });

    iconSelect = new IconSelect("cmE-widget",
        {'selectedIconWidth':75,
        'selectedIconHeight':75,
        'iconsWidth':75,
        'iconsHeight':75
        });

    var icons = [];

    icons.push({'iconFilePath':'/static/img/X.svg','iconValueMao':''});


////    var grupoCM = [];
//    $(function(){
//        for(CM.group){
//            icons.push({'iconFilePath':'/static/img/configuracoes_de_mao/'{CM.group}'/'{CM.group}'.png', 'iconValue': {CM.group}});
//        }
//    }
    iconSelect.refresh(icons);

};