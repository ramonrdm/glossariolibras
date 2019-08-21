  $(document).ready(function(){
    $('#modalCM').modal();
    $('#modalGrupos').modal();
    $('.botao').click(function(){
        var grupo = $(this).attr('id');
        alert(grupo);
    });


 });


