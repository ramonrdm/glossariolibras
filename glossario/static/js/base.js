$(document).ready(function() {
  $('input[type=checkbox]').each(function() {
    if(this.nextSibling.nodeName != 'label') {
      $(this).after('<label for="'+this.id+'"></label>')
    }
  });

         $('.pesquisaTexto').hide();

        $('#pesquisaTexto').click(function(){
        $('.pesquisaLibras').show()
        $('.pesquisaTexto').hide()

        });

      $('#pesquisaLibras').click(function(){
        $('.pesquisaTexto').show()
         $('.pesquisaLibras').hide()
        });



});

