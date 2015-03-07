/**
 * Created by Eric on 15/3/2.
 */
f = function() {
    if (typeof flask_pagedown_converter === "undefined")
        flask_pagedown_converter = Markdown.getSanitizingConverter().makeHtml;
    var md6 = document.createElement('div')
    md6.classNamd = 'col-md-6'
    var textarea = document.getElementById("flask-pagedown-%s");
    var preview = document.createElement('div');
    preview.className = 'flask-pagedown-preview';
    textarea.parentNode.insertBefore(preview, textarea.nextSibling);
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