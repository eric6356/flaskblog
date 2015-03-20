from wtforms.widgets import HTMLString, TextArea

pagedown_pre_html = '''
<div class="flask-pagedown">
'''

pagedown_post_html = '''
</div>
<script type="text/javascript">
f = function() {
    if (typeof flask_pagedown_converter === "undefined")
        flask_pagedown_converter = Markdown.getSanitizingConverter().makeHtml;
    var textarea = document.getElementById("flask-pagedown-%s");
    var preview = document.createElement('div');
    preview.className = 'flask-pagedown-preview col-md-6';
    textarea.style.cssText +=";overflow:hidden;";
    textarea.style.minHeight="200px";
    textarea.parentNode.parentNode.insertBefore(preview, textarea.parentNode.nextSibling);
    textarea.onkeyup = function() { preview.innerHTML = flask_pagedown_converter(textarea.value); }
    textarea.onkeyup.call(textarea);
}
if (document.readyState === 'complete') 
    f();
else if (window.addEventListener)
    window.addEventListener("load", f, false);
else if (window.attachEvent)
    window.attachEvent("onload", f);
else
    f();

var observe;
if (window.attachEvent) {
    observe = function (element, event, handler) {
        element.attachEvent('on'+event, handler);
    };
}
else {
    observe = function (element, event, handler) {
        element.addEventListener(event, handler, false);
    };
}
function init () {
    var text = document.getElementById('flask-pagedown-%s');
    function resize () {
        text.style.height = 'auto';
        text.style.height = text.scrollHeight+'px';
    }
    /* 0-timeout to get the already changed text */
    function delayedResize () {
        window.setTimeout(resize, 0);
    }
    observe(text, 'change',  resize);
    observe(text, 'cut',     delayedResize);
    observe(text, 'paste',   delayedResize);
    observe(text, 'drop',    delayedResize);
    observe(text, 'keydown', delayedResize);

    text.focus();
    text.select();
    resize();
}
window.onload=init();
</script>
'''

class PageDown(TextArea):
    def __call__(self, field, **kwargs):
        html = super(PageDown, self).__call__(field, id = 'flask-pagedown-' + field.name, class_ = 'flask-pagedown-input', **kwargs)
        html = '<div class="col-md-6" id="pagedown-input-col">' + html + '</div>'
        # print pagedown_pre_html + html + pagedown_post_html % field.name
        return HTMLString(pagedown_pre_html + html + pagedown_post_html % (field.name, field.name))
