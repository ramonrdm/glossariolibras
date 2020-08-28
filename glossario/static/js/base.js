$(document).ready(function () {
    $('.sidenav').sidenav();
    $('#fecharSidenav').hide();
    $('.tabs').tabs();


    $('.modal').modal();
    $('#confirmeEmail').modal('open');
    $('#confirmeEmailErro').modal('open');
    $('#login').modal('open');

    $('#abrirSidenav').click(function () {
        $('#abrirSidenav').hide();
        $('#fecharSidenav').show();
        $('.blockContainer').css({
            'padding-left': "16%"
        });
        $('.container').css({
            'padding-left': "10%"
        });
        $('.sidenav').css({
            width: "250px"
        });
    });

    $('#fecharSidenav').click(function () {

        $('#abrirSidenav').show();
        $('#fecharSidenav').hide();
        $('.blockContainer').css({
            'padding-left': "6%"
        });
        $('.container').css({
            'padding-left': "1%"
        });
        $('.sidenav').css({
            width: "79px"
        });
    });

    $('#abrirNavSearchMobile').click(function () {
        $('#mobileSearchLibras').hide();
        $('#mobileSearchEscrita').show();
    });

    $('#fecharNavSearchMobile').click(function () {
        $('#mobileSearchLibras').show();
        $('#mobileSearchEscrita').hide();
    });


    // Preview
    $('.preview').each(function (i) {
        $(this).prop('id', `preview-${i}`);

        var isFirst = true;

        $(`#preview-${i} img:gt(0)`).hide();
        $(`#preview-${i}`).hover(function () {
            if (isFirst) {
                timer = setInterval(function () {
                    $(`#preview-${i} :first-child`).fadeOut()
                        .next('img').fadeIn()
                        .end().appendTo(`#preview-${i}`);
                },
                    800);
                isFirst = false;
            }
        }, function () {
            clearInterval(timer);
            isFirst = true;
        });
    })
});