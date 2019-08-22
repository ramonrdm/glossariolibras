$(document).ready(function(){

$('.sidenav').sidenav();
$('#telaMobile').show();
$('.pesquisaViewModule').hide();
$('#mobileSearchEscrita').hide();


    if ((window.screen.availWidth < 800)){
    alert('passei aqui');
        $('#telaWeb').hide();
        $('#telaMobile').show();
        $('.sidenav').css({ 'z-index' : "1000"});
        $('.sidenav').css({ 'padding-top' : "0%"});
        $('.blockContainer').css({ 'padding-left': "0%"});
        $('.container').css({ 'padding-left': "1%"});
        $('.sidenav').css({ width: "80%"});

   }else{
        $('#telaMobile').hide();
        $('#telaWeb').show();
   }

    $('.modal').modal();
    $('#confirmeEmail').modal('open');
    $('#confirmeEmailErro').modal('open');
    $('#login').modal('open');
    $('#fecharSidenav').hide();

    $('#abrirSidenav').click(function(){
           $('#abrirSidenav').hide();
           $('#fecharSidenav').show();
           $('.blockContainer').css({ 'padding-left': "16%"});
           $('.container').css({ 'padding-left': "10%"});
           $('.sidenav').css({ width: "250px"});
    });

    $('#fecharSidenav').click(function(){
           $('#abrirSidenav').show();
           $('#fecharSidenav').hide();
           $('.blockContainer').css({ 'padding-left': "6%"});
           $('.container').css({ 'padding-left' : "1%"});
           $('.sidenav').css({ width: "79px"});
     });


    $('#buttonViewModule').click(function(){
           $('.pesquisaViewList').hide();
           $('.pesquisaViewModule').show();
    });

    $('#buttonViewList').click(function(){
           $('.pesquisaViewList').show();
           $('.pesquisaViewModule').hide();
     });



    $('#buttonViewModuleMobile').click(function(){
           $('.pesquisaViewList').hide();
           $('.pesquisaViewModule').show();
    });

    $('#buttonViewListMobile').click(function(){
           $('.pesquisaViewList').show();
           $('.pesquisaViewModule').hide();
     });




    $('#abrirNavSearchMobile').click(function(){
           $('#mobileSearchLibras').hide();
           $('#mobileSearchEscrita').show();

    });

    $('#fecharNavSearchMobile').click(function(){
           $('#mobileSearchLibras').show();
           $('#mobileSearchEscrita').hide();

     });


  $(document).ready(function(){
    $('.tabs').tabs();
  })

});

