document.addEventListener('DOMContentLoaded',()=>{
  document.querySelectorAll('.edit_button').forEach(function(button){
    button.onclick=function(){
      document.getElementById(`content${button.id}`).style='display:none;';
      var edit_box=document.createElement('textarea');
      edit_box.style='width:700px; height:80px;';
      document.getElementById(`content_area${button.id}`).append(edit_box);
      fetch('/posts/'+button.id)
      .then(response => response.json())
      .then(post => {
        edit_box.value=post.content;
      }
    );
    button.style='display:none;';
    var save_button=document.createElement('button');
    save_button.textContent='Save Changes';
    document.getElementById(`edit_button_area${button.id}`).append(save_button);
    save_button.onclick=function(){
      fetch('/posts/'+button.id, {
        method: 'PUT',
        body: JSON.stringify({
          content:edit_box.value,
        })
      })
      edit_box.style='display:none;';
      save_button.style='display:none;';
      document.getElementById(`content${button.id}`).textContent=edit_box.value;
      document.getElementById(`content${button.id}`).style='display:block;';
      button.style='display:block;';
    }
  }
});
//////////////////////////////////////
document.querySelectorAll('.like_button').forEach(function(button){
  button.onclick=function(){
    document.getElementById(`like_count${button.id}`).textContent= parseInt(document.getElementById(`hidden_count${button.id}`).value)+1;
    fetch('/posts/like/'+button.id, {
      method: 'PUT',
      body: JSON.stringify({
        like:document.getElementById(`like_count${button.id}`).textContent,
        liked_post:button.id,
      })
    })
    button.style='display:none;'
    var liked_message = document.createElement('p')
    liked_message.textContent='You just liked this post! Refresh the page to be able to unlike.'
    document.getElementById(`like_button_area${button.id}`).append(liked_message)
}
});
document.querySelectorAll('.unlike_button').forEach(function(button){
  button.onclick=function(){
    document.getElementById(`like_count${button.id}`).textContent= parseInt(document.getElementById(`hidden_count${button.id}`).value)-1;
    fetch('/posts/unlike/'+button.id, {
      method: 'PUT',
      body: JSON.stringify({
        like:document.getElementById(`like_count${button.id}`).textContent,
        liked_post:button.id,
      })
    })
    button.style='display:none;'
    var unliked_message = document.createElement('p')
    unliked_message.textContent='You just unliked liked this post! Refresh the page to be able to like it again.'
    document.getElementById(`like_button_area${button.id}`).append(unliked_message)
}
});
});
