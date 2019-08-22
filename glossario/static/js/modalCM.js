  $(document).ready(function(){
    $('.modalCM').modal();
    $('.modalGrupos').modal();

    $('.escolhaGrupo').click(function(){
        var escolhaGrupo = $(this).attr('id');
        alert(escolhaGrupo);;

    });

   $('.escolhaCM').click(function(){
        var escolhaCM = $(this).attr('id');
         alert(escolhaCM);;

    });

   $('.testeBotaoMobile').click(function(){
        alert('fui apertado');
   });

 });
