$(document).ready(function(){
    $('.modal').modal();
    var valor_movimentacao = JSON.parse(document.getElementById('valor_movimentacao').textContent);
    if(valor_movimentacao){
        $('#imagem_movimentacao').attr('src', $("#imagem_movimentacao_"+valor_movimentacao).attr('src'));
        if (valor_movimentacao != 0) {
            $('#id_movimentacao').val(valor_movimentacao);
        } else {
            $('#id_movimentacao').val('');
        }
    }
    $('.escolhaMovimentacao').click(function(){
        var escolhaMovimentacao = $(this).attr('id-field');
        $('#imagem_movimentacao').attr('src', $(this).attr('src'));
        if (escolhaMovimentacao != 0) {
            $('#id_movimentacao').val(escolhaMovimentacao);
        } else {
            $('#id_movimentacao').val('');
        }
    });
});