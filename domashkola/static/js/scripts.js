function myFunc(vars) {
    return vars
}


function isMobile() {
    const isTouchScreen = "ontouchstart" in window || navigator.maxTouchPoints > 0;
    const isSmallScreen = window.innerWidth < 768; // Обычно мобильные устройства имеют ширину меньше 768px, но это не точно
    return isTouchScreen && isSmallScreen;
}

//Функция формирует url после ввода номера страницы на странице pagination.html
function get_url(inputed_page) {
    var url = window.location.href;
    var i = url.indexOf("=");
    var result_url = '';
    
    switch (i) {
        case -1:
            result_url = url + '?page=' + inputed_page;
            break;
        default:
            result_url = url.substring(0, i+1) + inputed_page;
    }
    return result_url;
}