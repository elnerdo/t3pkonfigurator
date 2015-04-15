function set_body_size() {
    var h = $(window).height();
    $('body').css('height', h);
}

function set_background() {
    var w = $('#canvas-div').width() * 0.8;
    var h = $(window).height() * 0.8;
    $('#myCanvas').attr('width', w);
    $('#myCanvas').attr('height', h);  
    setTimeout(draw_background, 100);
}

function draw_background() {
    var c = document.getElementById('myCanvas');
    var ctx = c.getContext("2d");
    var background = document.getElementById("background");
    ctx.drawImage(background, 0, 0, set_background_width(), set_background_height());
}

function set_background_width() {
    var w = $('#myCanvas').width();
    return w;
}

function set_background_height() {
    var h = $('#myCanvas').height();
    return h;
}

function set_elements(elements, tube, depths) {
    setTimeout( function() {
        draw_elements(elements, tube, depths)
    }, 100)   
}

function draw_elements(elements, tube, depths) {
    var c = document.getElementById('myCanvas');
    var ctx = c.getContext("2d");
    var offset = set_tube_offset_y((tube/100) + 1) + 25;
    var counter = 0
    for(x=0;x<elements.length;x++) {
        var element = document.getElementById("img-" + elements[x]);
        height = $(element).attr('height') * 1/6 * $('#myCanvas').height() / 100;
        offset = offset - height - 2;
        ctx.drawImage(element, set_offset_x() + 5, offset, 20, height);
        if (elements[x] == 'probe') {
            ctx.fillStyle="#eee";
            ctx.fillRect(set_offset_x() + 50, offset + 5, 50, 20);
            ctx.fillStyle="green";
            console.log(ctx.font);
            ctx.font = '12pt sans-serif';
            ctx.fillText(depths[counter], set_offset_x() + 60, offset + 20);
            counter += 1;
        }
    }
}

function set_tubehead() {
    setTimeout(draw_tubehead, 100);
}

function draw_tubehead() {
    var c = document.getElementById('myCanvas');
    var ctx = c.getContext("2d");
    var tubehead = document.getElementById('tubeimg-top');
    ctx.drawImage(tubehead, set_offset_x(), set_tubehead_offset_y(), set_width(), 75);
}

function set_tube(tubelen) {
    setTimeout( function() {
        draw_tube(tubelen)
    }, 100)
}

function draw_tube(tubelen) {
    var c = document.getElementById('myCanvas');
    var ctx = c.getContext("2d");
    var tube = document.getElementById('tubeimg-100');
    var runs = tubelen / 100;
    for (x=1;x<=runs;x++) {
        ctx.drawImage(tube, set_offset_x(), set_tube_offset_y(x), set_width(), set_tube_height());
    }
    var tubeend = document.getElementById('tubeimg-bottom');
    ctx.drawImage(tubeend, set_offset_x(), set_tube_offset_y(runs+1), set_width(), 75);
}

function set_tubehead_offset_y() {
    var mycanvas = document.getElementById('myCanvas');
    var rect = mycanvas.getBoundingClientRect();
    return rect.height * 0.3;
}

function set_offset_x() {
    var mycanvas = document.getElementById('myCanvas');
    var rect = mycanvas.getBoundingClientRect();
    return (rect.width / 2) - 25;
}

function set_tube_offset_y(x) {
    var mycanvas = document.getElementById('myCanvas');
    var rect = mycanvas.getBoundingClientRect();
    return (rect.height / 3) + (set_tube_height() * (x - 1));
}

function set_xval() {
    var  w = $('#myCanvas').width();
    return w / 2 - 20;
}

function set_yval(bla) {
    var h = $('#myCanvas').height();
    return bla + 100;
}

function set_width() {
    return 35;
}

function set_tube_height() {
    return $('#myCanvas').height() * 1/6;
}
