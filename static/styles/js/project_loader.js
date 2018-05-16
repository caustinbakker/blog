const projectheader = document.querySelectorAll('.project_l > header, .project_r > header ')
const projectheaderstart = []

for (var i = 0; i < projectheader.length; i++) {
    projectheaderstart[i] = projectheader[i].offsetTop;
    // projectheader[i].style.flexBasis = '100%';
}

document.addEventListener('scroll', () =>{
    for (var i = 0; i < projectheader.length; i++) {
        if (projectheaderstart[i] <= (window.scrollY*2)) {
            projectheader[i].classList.remove('project_loader')
        }else{
            projectheader[i].classList.add('project_loader')
        }
    }
});

// if (projectheaderstart[i] <= (window.scrollY*2)) {
//     projectheader[i].style.flexBasis = '0%';
// }else{
//     projectheader[i].style.flexBasis = '100%';
// }
