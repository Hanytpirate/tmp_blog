var onResize = function() {
    // apply dynamic padding at the top of the body according to the fixed navbar height
    $("body").css("padding-top", parseInt($(".navbar.fixed-top").height())+2*parseInt($(".navbar.fixed-top").css('padding-top')));
    $("body").css("padding-bottom", parseInt($(".navbar.fixed-bottom").height())+2*parseInt($(".navbar.fixed-bottom").css('padding-bottom')));
};

// attach the function to the window resize event
$(window).resize(onResize);
var attach_send_new_article = function() {
    $("#send_new_article").click(function() {
        // $("#textInput").val() 
        var form = $("<form>").attr("method", "post").attr("action", window.location.pathname);
        $("<input>")
        .attr("type", "hidden")
        .attr("name", "article-content") // 设置字段名
        .attr("value", document.getElementById('content').innerText) // 设置字段值
        .appendTo(form);
        a = document.getElementById('#new_article_title')
        // a.appendTo(form)
        $("#new_article_title").appendTo(form)
        // alert($("#new_article_title").name)

        form.appendTo("body").submit()
        
        
    })
};
var load_content_for_update = function(){
    var re = new RegExp("/post/\\d+/update");
    var red = new RegExp("\\d+")
    console.log(window.location.pathname.split(red))
    console.log(re.test(window.location.pathname))
    if(re.test(window.location.pathname)){
        $.ajax({
            type: 'GET',
            url: window.location.pathname,
            data:{have:true},
            success: function(res){
                console.log(res)
            },
            error: function(){
                consle.log('error')
            }
        });
    }
}
// call it also when the page is ready after load or reload
$(function() {
    onResize();
    attach_send_new_article()
    load_content_for_update()
});

if(document.getElementById('content')!== null){
    var vditor = null;
    window.onload = function() {
        vditor = new Vditor(document.getElementById('content'), {
            cache: {
                enable: false
            },
            "mode": "ir"
        });
    }     
}
