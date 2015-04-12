/**
 * Created by Eric on 15/4/12.
 */
function show_comment(what){
    var comment_form = what.parentNode.parentNode.nextSibling.nextSibling;
    if(comment_form.style.display=="none"){
        comment_form.style.display="";
    }
    else{
        comment_form.style.display="none";
    }
}

function get_date_string(){
    var dateObj = new Date();
    var year = dateObj.getFullYear();
    var month = dateObj.getMonth()+1;
    if (month < 10) month = '0' + month;
    var date = dateObj.getDate();
    var hour = dateObj.getHours();
    if (hour < 10) hour = '0' + hour;
    var minute = dateObj.getMinutes();
    if (minute < 10) minute = '0' + minute;
    return year + '-' + month + '-' + date + ' ' + hour + ':' + minute + ', 新评论';
}


function submit_comment(what, author, author_name, post, commented){
    var sc = document.body.scrollTop;
    var content = what.parentNode.parentNode.previousSibling.previousSibling.value;
    $.post('/api/comment.json', {'author': author, 'post': post, 'commented': commented, 'content': content}, function (result){
        console.log(result);
    });
    var new_comment = document.createElement('div');
    new_comment.setAttribute('class', 'post-sub-comment');

    var author_div = document.createElement('div');
    author_div.setAttribute('class', 'post-comment-author');
    author_div.textContent = author_name;
    new_comment.appendChild(author_div);

    var content_div = document.createElement('div');
    content_div.setAttribute('class', 'post-comment-content');
    content_div.textContent = content;
    new_comment.appendChild(content_div);

    var date_div = document.createElement('div');
    date_div.setAttribute('class', 'post-comment-date');

    date_div.textContent = get_date_string();
    new_comment.appendChild(date_div);

    if(post!=commented){
        console.log('comment on comment');
        what.parentNode.parentNode.parentNode.parentNode.parentNode.appendChild(new_comment);
        what.parentNode.parentNode.parentNode.parentNode.style.display = 'none'
    }
    else {
        console.log('comment on pot');
        var comment_div = document.getElementsByClassName('post-comment')[0];
        comment_div.insertBefore(new_comment, comment_div.lastChild.previousSibling);
        //var form_node = what.parentNode.parentNode.parentNode.parentNode.parentNode;
        //form_node.insertBefore(form_node, new_comment);
    }
    document.body.scrollTop = sc;

}

function delete_comment(what, post, commented){
    var content = what.parentNode.parentNode.previousSibling.previousSibling.value;
    console.log(post);
    console.log(commented);
    $.ajax({
        url: '/api/comment.json',
        type: 'PUT',
        data: {'post': post, 'commented':commented},
        success: function(response) {
            what.parentNode.parentNode.previousSibling.previousSibling.textContent = 'This comment has been deleted...'
       }
    });
}