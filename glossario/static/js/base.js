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

    // Lazy Loading images
    if ('loading' in HTMLImageElement.prototype) {
        const images = document.querySelectorAll("img.lazyload");
        images.forEach(img => {
            img.src = img.dataset.src;
        });
    } else {
        // Dynamically import the LazySizes library if browser doesnt support
        let script = document.createElement("script");
        script.async = true;
        script.src =
            "https://cdnjs.cloudflare.com/ajax/libs/lazysizes/4.1.8/lazysizes.min.js";
        document.body.appendChild(script);
    }

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
    });
});