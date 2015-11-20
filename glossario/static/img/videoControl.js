window.onload = function() {
    document.getElementsByTagName('video')[0].onclick = function(){
        var video = document.getElementsByTagName('video')[0];
        if(video.paused)
            video.play();
        else
            video.pause();
    }
    document.getElementById("pause").onclick = function() {
        //        alert("pause");
        document.getElementsByTagName('video')[0].pause();
    };

    document.getElementById("play").onclick = function() {
        //        alert("play");
        document.getElementsByTagName('video')[0].play();
    };


    //    $("img#play").click(function() {
    //        //			alert("play");
    //        $("#videoplay").get(0).play();
    //    });

    document.getElementById("stop").onclick = function() {
        //        alert("stop");
        document.getElementsByTagName('video')[0].currentTime=0;
        document.getElementsByTagName('video')[0].pause();
    };

//    $("img#stop").click(function() {
//        //                        alert("stop");
//        $("#videoplay").get(0).currentTime=0;
//        $("#videoplay").get(0).pause();
//    });

};