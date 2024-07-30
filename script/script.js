document.querySelectorAll(".buy-now").forEach(element => {
    element.addEventListener('mouseenter', function () {
        element.parentElement.querySelector('.info').classList.add('blurred');
    });

    element.addEventListener('mouseleave', function () {
        element.parentElement.querySelector('.info').classList.remove('blurred');
    });
})