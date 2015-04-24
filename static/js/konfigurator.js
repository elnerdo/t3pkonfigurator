function check_form(requiredValues) {
    for (i=0; i < requiredValues.length; i++) {
        var foo = $(requiredValues[i])[0];
        if (foo.value === '') {
            event.preventDefault();
            $(foo).addClass('missing-required');
        }        
    }
    return;
}

function submit_form(form) {
    var inputs = $(form + ' :input');
    var valid = true;
    var valid_pattern = true;
    event.preventDefault();
    for (var i=0; i < inputs.length; i++) {
        if (inputs[i].id == 'add-btn') {
            continue;
        }
        if (inputs[i].value === '') {
            $(inputs[i]).addClass('missing-required');
            
            valid = false;
        }
        else {
            if (inputs[i].pattern) {
                valid_pattern = check_pattern(inputs[i]);
            }
            else {
                $(inputs[i]).removeClass('missing-required');
            }
        }
    }
    if (valid && valid_pattern) {
        $(form).submit();
    }
    return;
}

function check_pattern(input) {
    var pattern = /^[0-9]+$/;
    var matched = pattern.test(input.value);
    if (matched) {
        $(input).removeClass('missing-required');
        return true;
    }

    $(input).addClass('missing-required');
    return false
}

function set_body_size() {
    var h = $(window).height();
    $('body').css('min-height', h);
}

function set_background() {
    var w = $('#canvas-div').width();
    var h = $(window).height() * 0.8;
    $('#myCanvas').attr('width', w);
    $('#myCanvas').attr('height', h);
    var h2 = h + 8;
    $('#data-div').css('min-height', h2 + 'px');
    draw_background();
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
    $('#img-probe, #img-spacer10, #img-spacer30, #img-spacer80').ready(function() {
        draw_elements(elements, tube, depths);
    });
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
            ctx.fillRect(set_offset_x() - 50, offset + 5, 50, 20);
            ctx.fillStyle="green";
            ctx.font = '12pt sans-serif';
            ctx.fillText(depths[counter], set_offset_x() - 40, offset + 20);
            counter += 1;
        }
    }
}

function set_tubehead() {
    $('#tubeimg-top').ready(function() {
        draw_tubehead();
    });
}

function draw_tubehead() {
    var c = document.getElementById('myCanvas');
    var ctx = c.getContext("2d");
    var tubehead = document.getElementById('tubeimg-top');
    ctx.drawImage(tubehead, set_offset_x(), set_tubehead_offset_y(), set_width(), 75);
}

function set_tube(tubelen) {
    $('#tubeimg-100').ready(function() {
        draw_tube(tubelen);
    });
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

function help_msg() {
    $('#pdf_msg').text('PDF erstellt.');
    $('#pdf_msg').css('visibility', 'visible');
}
