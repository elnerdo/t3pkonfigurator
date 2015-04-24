function set_resolution(w, h) {
    $('body').height(h);
    $('body').width(w);
    var content = "width=" + w + ", height=" + h + ", initial-scale=1.0";
    $('#viewport').attr('content', content);
    //$('#container').css({width: w, height: h});
}
