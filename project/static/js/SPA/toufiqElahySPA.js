$.fn.toufiqSPA=function(t){var r=$(this);window.history&&window.history.pushState&&$(window).on("popstate",function(){var t=window.location.href;-1==t.indexOf("#")&&(r.addClass("spa-loader"),
    $.ajax({type:"get",url:t,success:function(t,o,e){console.log("hummm"), r.removeClass("spa-loader"),r.html(t)},error:function(t,o,e){r.removeClass("spa-loader"),"error"==o&&alert(t)}}))}),
    $(document).on("submit","form:not(.stopAjax)",
        function(t){
        t.preventDefault();
        var l=$(this),
            a=l.attr("action");
        ""==a&&(a=window.location.href)
        var o=l.attr("method"),
            e=new FormData(this),n=l.attr("ajax-target");
        (n=null==n?r:$(n)).addClass("spa-loader"),
    "post"==o.toLowerCase()?
    $.ajax({type:o,
        url:a,
        data:e,
        processData:!1,
        contentType:!1,
        success:function(t,o,e){
                console.log("na me this")
                n.removeClass("spa-loader"),
                null!=l.attr("eval")||(n==r&&(a=e.getResponseHeader("Location"))!=window.location.href.toString().split(window.location.host)[1]&&window.history.pushState(null,null,a),n.html(t))},
            error:function(t,o,e){n.removeClass("spa-loader"),n.html(t),"error"==o&&alert(t)}}):$.ajax({type:o,url:a+"?"+l.serialize(),success:function(t,o,e){n.removeClass("spa-loader"),null!=l.attr("eval")||(n==r&&(a=e.getResponseHeader("Location"))!=window.location.href.toString().split(window.location.host)[1]&&window.history.pushState(null,null,a),n.html(t))},error:function(t,o,e){n.removeClass("spa-loader"),n.html(t),"error"==o&&alert(t)}})}),
    $(document).on("click",'a[href^="/"]:not(.stopAjax),button[href],input[href]',function(t){var l=$(this),a=l.attr("href"),n=l.attr("ajax-target");(n=null==n?r:$(n)).addClass("spa-loader"),$.ajax({type:"get",url:a,success:function(t,o,e){console.log('gggg'), n.removeClass("spa-loader"),null!=l.attr("eval")||(n==r&&(a=e.getResponseHeader("Location"))!=window.location.href.toString().split(window.location.host)[1]&&window.history.pushState(null,null,a),n.html(t))},error:function(t,o,e){n.removeClass("spa-loader"),"error"==o&&alert(t),window.history.pushState(null,null,a)}}),t.preventDefault()})};