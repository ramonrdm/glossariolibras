$(document).ready(function(){
    $('.modal').modal();
    $('.escolhaCM').click(function(){
         var escolhaCM = $(this).attr('id');
         $('#id_cmE').val(escolhaCM);
         $('#image_cm').attr('src', $(this).attr('src'));

     });



});

