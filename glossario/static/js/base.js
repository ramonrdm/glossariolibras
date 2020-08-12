$(document).ready(function () {
    $('.sidenav').sidenav();
    $('#fecharSidenav').hide();
    $('.tabs').tabs();


    $('.modal').modal();
    $('#confirmeEmail').modal('open');
    $('#confirmeEmailErro').modal('open');
    $('#login').modal('open');

    $('#abrirSidenav').click(function () {
        $('#abrirSidenav').hide();
        $('#fecharSidenav').show();
        $('.blockContainer').css({
            'padding-left': "16%"
        });
        $('.container').css({
            'padding-left': "10%"
        });
        $('.sidenav').css({
            width: "250px"
        });
    });

    $('#fecharSidenav').click(function () {

        $('#abrirSidenav').show();
        $('#fecharSidenav').hide();
        $('.blockContainer').css({
            'padding-left': "6%"
        });
        $('.container').css({
            'padding-left': "1%"
        });
        $('.sidenav').css({
            width: "79px"
        });
    });

});