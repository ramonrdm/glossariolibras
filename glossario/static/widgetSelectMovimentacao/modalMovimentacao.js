$(document).ready(function(){


    $('.escolhaMovimentacao').click(function(){
         var escolhaMovimentacao = $(this).attr('id');
         $('#id_movimentacao').val(escolhaMovimentacao);
         $('#image_movimentacao').attr('src', $(this).attr('src'));

     });

});