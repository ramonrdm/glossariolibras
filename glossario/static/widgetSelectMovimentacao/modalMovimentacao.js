$(document).ready(function(){
    $('.modal').modal();
    $('.escolhaMovimentacao').click(function(){
         var escolhaMovimentacao = $(this).attr('id-field');
         $('#id_movimentacao').val(escolhaMovimentacao);
         $('#imagem_movimentacao').attr('src', $(this).attr('src'));
         $('#imagem_movimentacao_mobile').attr('src', $(this).attr('src'));
     });
});
