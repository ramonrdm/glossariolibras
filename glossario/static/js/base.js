
$(document).ready(function() {
  $('input[type=checkbox]').each(function() {
    if(this.nextSibling.nodeName != 'label') {
      $(this).after('<label for="'+this.id+'"></label>')
    }
  });

        $('#Texto').hide();

        $('#pesquisaTexto').click(function(){
        $('#Libras').show()
        $('#Texto').hide()

        });

      $('#pesquisaLibras').click(function(){
        $('#Texto').show()
         $('#Libras').hide()
        });


});

