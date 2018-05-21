const file = document.querySelector('#file').files[0]
const imagepreview = document.querySelector('#imagepreview')
document.addEventListener('change', () => {
    console.log(URL.createObjectURL(file.value));
    imagepreview.src = file.preview;
})
