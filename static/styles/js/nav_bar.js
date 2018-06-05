var nav_bar = document.querySelector('#nav_bar')
var nav_bar_start = (nav_bar.offsetTop);


function nav_bar_js(){
    if (nav_bar_start < (window.scrollY)) {
        nav_bar.classList.add('nav_bar_fixed');
    }else{
        nav_bar.classList.remove('nav_bar_fixed');
    }
}
document.addEventListener('scroll', nav_bar_js);
