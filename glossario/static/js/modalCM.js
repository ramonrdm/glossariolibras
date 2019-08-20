  $(document).ready(function(){
    $('.modalCM').modal();
    $('.modalGrupos').modal();



    $('#modalGrupos').click(function(){
        var images = $('#modal-content img').attr('id');
        alert(images);
    });


 });


