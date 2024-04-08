var onResize = function() {
    // apply dynamic padding at the top of the body according to the fixed navbar height
    $("body").css("padding-top", parseInt($(".navbar.fixed-top").height())+2*parseInt($(".navbar.fixed-top").css('padding-top')));
    $("body").css("padding-bottom", parseInt($(".navbar.fixed-bottom").height())+2*parseInt($(".navbar.fixed-bottom").css('padding-bottom')));
};

// attach the function to the window resize event
$(window).resize(onResize);
var attach_send_new_article = function() {
    $("#send_new_article").click(function() {
        
    })
};

// call it also when the page is ready after load or reload
$(function() {
    onResize();
    
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
