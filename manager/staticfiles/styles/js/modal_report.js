var body = document.querySelector('.body');
var icon = document.querySelector('.delete_report');

icon.addEventListener('click', function(e) {   
    body.classList.add('modal-open');
});