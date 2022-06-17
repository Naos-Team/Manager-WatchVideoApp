var check = document.getElementById('toggle-dark');
var body = document.querySelector('.body');
check.addEventListener('click', function(e) {   
    if (check.checked) {
        if (body.classList.contains('theme-light')){
            body.classList.remove('theme-light');
            body.classList.add('theme-dark');
        }
    }
    else{
        if (body.classList.contains('theme-dark')){
            body.classList.remove('theme-dark');
            body.classList.add('theme-light');
        }
    }
});

var ul = window.location.href.toString();
if (ul.includes( 'dashboard')){
    document.querySelector('.dashboard').classList.add('active');
}
else if(ul.includes( 'category')){
    document.querySelector('.category').classList.add('active');
}
 