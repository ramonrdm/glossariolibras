$(document).ready(function(){
    $('.modal').modal();
    var valor_movimentacao = JSON.parse(document.getElementById('valor_movimentacao').textContent);
    if(valor_movimentacao){
        $('#id_movimentacao').val(valor_movimentacao);
        $('#imagem_movimentacao').attr('src', $("#imagem_movimentacao_"+valor_movimentacao).attr('src'));
    }
    $('.escolhaMovimentacao').click(function(){
        var escolhaMovimentacao = $(this).attr('id-field');
        $('#id_movimentacao').val(escolhaMovimentacao);
        $('#imagem_movimentacao').attr('src', $(this).attr('src'));
    });
});