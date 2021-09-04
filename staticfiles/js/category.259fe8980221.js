$(document).ready(function () {

    function subshow(subtype) {
        if (subtype.classList.contains('hidden')) {
            subtype.classList.toggle('hidden');
            setTimeout(function () {
                subtype.classList.toggle('visuallyhidden');
            });
        } else {
            subtype.classList.toggle('visuallyhidden');
            subtype.addEventListener('transitionend', function (e) {
                subtype.classList.toggle('hidden');
            }, {
                capture: false,
                once: true,
                passive: false
            });
        }
    }

    let datasub = document.getElementById('datasub');
    btn = document.getElementById('data');

    let websub = document.getElementById('websub');
    btn1 = document.getElementById('web');

    let mobilesub = document.getElementById('mobilesub');
    btn2 = document.getElementById('mobile');

    let gamesub = document.getElementById('gamesub');
    btn3 = document.getElementById('game');


    btn.addEventListener('click', function () {
        let dataInfo = document.getElementById('dataInfo')
        dataInfo.classList.toggle('hidden')
        subshow(datasub)
    });
    btn1.addEventListener('click', function () {
        let webInfo = document.getElementById('webInfo')
        webInfo.classList.toggle('hidden')
        subshow(websub)
    });
    btn2.addEventListener('click', function () {
        let mobileInfo = document.getElementById('mobileInfo')
        mobileInfo.classList.toggle('hidden')
        subshow(mobilesub)
    });
    btn3.addEventListener('click', function () {
        let gameInfo = document.getElementById('gameInfo')
        gameInfo.classList.toggle('hidden')
        subshow(gamesub)
    
    });

});