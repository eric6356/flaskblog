/**
 * Created by Eric on 15/4/4.
 */
$(document).ready(function () {
    console.log('========');
    $.getJSON("/api/hot_tags", {"n": 5}, function(result){
        if (result['code']==200) {
            ul = document.getElementById('hot_tags');
            $.each(result['data'], function(i, field){
                a = document.createElement('a');
                a.setAttribute('class', 'nounderline label label-primary');
                a.href = '/tags/'+field[0];
                a.innerText = field[0] + '(' + field[1] + ')';
                li = document.createElement('li');
                li.appendChild(a);
                ul.appendChild(li);
            });
        };
    });
    $.getJSON("/api/recent_posts", {'n': 3}, function (result) {
        if (result['code'] == 200) {
            ul = document.getElementById('recent_posts');
            $.each(result['data'], function (index, field) {
                a = document.createElement('a');
                a.href = '/post/' + index;
                a.innerText = field;
                li = document.createElement('li');
                li.appendChild(a);
                ul.appendChild(li);
            })
        }
    })
});
