const nav_bar = document.querySelector('#nav_bar')
const nav_bar_start = nav_bar.offsetTop;


function nav_bar_js(){
    if (nav_bar_start < window.scrollY) {
        nav_bar.classList.add('nav_bar_fixed');
    }else if (nav_bar_start >= window.scrollY){
        nav_bar.classList.remove('nav_bar_fixed');
    }
}

document.addEventListener('scroll', nav_bar_js);
