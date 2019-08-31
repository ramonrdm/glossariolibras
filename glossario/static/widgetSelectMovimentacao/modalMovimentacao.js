$(document).ready(function(){
    $('.modal').modal();
    $('.escolhaMovimentacao').click(function(){
         var escolhaMovimentacao = $(this).attr('id');
         $('#id_movimentacao').val(escolhaMovimentacao);
         $('#image_movimentacao').attr('src', $(this).attr('src'));
         $('#image_movimentacao_mobile').attr('src', $(this).attr('src'));

     });

});
