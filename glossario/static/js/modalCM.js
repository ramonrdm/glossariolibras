  $(document).ready(function(){
    $('.modalCM').modal();
    $('.modalGrupos').modal(
        startingTop = '100%'
    );

    $('.escolhaGrupo').click(function(){
        var escolhaGrupo = $(this).attr('id');

    });

   $('.escolhaCM').click(function(){
        var escolhaCM = $(this).attr('id');

    });


 });


