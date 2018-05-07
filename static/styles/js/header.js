

const headerlist = document.querySelectorAll('.header_title');
let header_start_height = [];

for (let i = 0; i < headerlist.length; i++){

    let startheight = (headerlist[i].offsetTop - headerlist[i].getBoundingClientRect().height);
    const elementStartHeight = headerlist[i].offsetTop;
    document.addEventListener('scroll', () => {
            var Eheight = (headerlist[i].offsetTop - headerlist[i].getBoundingClientRect().height)
            var minheight = (headerlist[i].getBoundingClientRect().height / 1.5)
            var distancetravelt = startheight;

            if ((elementStartHeight+70) <= headerlist[i].offsetTop) {
                headerlist[i].classList.add('header_title_fixed');
            }else if ((elementStartHeight+30) >= headerlist[i].offsetTop){
                headerlist[i].classList.remove('header_title_fixed')
            }
        });
}
