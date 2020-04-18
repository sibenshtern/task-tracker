function activate_element(element) {
    alert(element);
    $(element).toggleClass('active');
}

function set_window_location(element) {
    window.location = $(this).find('a').attr('href');
}

$(document).ready(function () {
    $('#sidebarCollapse').on('click', activate_element);
    $('.sidebar-component').on('click', set_window_location);
});

let path = window.location.toString().split('/').pop();
alert(path);
activate_element("#" + path);



