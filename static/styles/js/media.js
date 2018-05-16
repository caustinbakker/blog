const postslist = document.querySelectorAll('li.post_media')

var active_media = []
var posts = []

for (var i = 0; i < postslist.length; i++) {
    posts[i] = postslist[i].querySelectorAll('figure > img');
    var button = postslist[i].querySelector('article > button');
    button.setAttribute( "onClick", 'media_selector('+String(i)+')');
    active_media[i] = 0;
}

function media_selector(post_id){
    if ((active_media[post_id]+1) < posts[post_id].length) {
        active_media[post_id]++;
    }else{
        active_media[post_id] = 0;
    }
    media_changer(post_id)
}

function media_changer(post_id){
    let images = posts[post_id];
    for (var i = 0; i < images.length; i++) {
        if (active_media[post_id] == i) {
            images[i].style.display = 'Block'
        }else{
            images[i].style.display = 'None'
        }
    }


}

for (var i = 0; i < posts.length; i++) {
    media_changer(i);
}

while (true) {
    setTimeout(function(){
    if(newState == -1){alert('VIDEO HAS STOPPED');}
}, 5000);
}
