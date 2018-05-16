const project_list = document.querySelector('#projects')
const project_list_start = project_list.offsetTop;
console.log(project_list_start)
function projects_js(){
    if (project_list_start < window.scrollY) {
        project_list.classList.add('projects_fixed');
    }else if (project_list_start >= window.scrollY){
        project_list.classList.remove('projects_fixed');
    }
    console.log(project_list_start < window.scrollY)
}

document.addEventListener('scroll', projects_js);
