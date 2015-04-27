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

function loadImages(sources, callback) {
        var images = {};
        var loadedImages = 0;
        var numImages = 0;
        // get num of sources
        for(var src in sources) {
          numImages++;
        }
        for(var src in sources) {
          images[src] = new Image();
          images[src].onload = function() {
            if(++loadedImages >= numImages) {
              callback(images);
            }
          };
          images[src].src = sources[src];
        }
}

function draw_canvas(elements, tube, depths) {
    set_background_size();
    var c = document.getElementById('myCanvas');
    var ctx = c.getContext("2d");
    var sources = {
        background: '/t3pkonfigurator/static/background.png',
        top: '/t3pkonfigurator/static/PROFILE_top.png',
        tube: '/t3pkonfigurator/static/PROFILE_leer_100.png',
        bottom: '/t3pkonfigurator/static/PROFILE_bottom.png',
        probe: '/t3pkonfigurator/static/probe.png',
        spacer10: '/t3pkonfigurator/static/spacer10.png',
        spacer30: '/t3pkonfigurator/static/spacer30.png',
        spacer80: '/t3pkonfigurator/static/spacer80.png'
    } 
        
    if (depths.length > 0) {
        loadImages(sources, function(images) {
            ctx.drawImage(images.background, 0, 0, set_background_width(), set_background_height());
            ctx.drawImage(images.top, set_offset_x(), set_tubehead_offset_y(), set_width(), 75);

            var runs = tube / 100;
            for (x=1;x<=runs;x++) {
                ctx.drawImage(images.tube, set_offset_x(), set_tube_offset_y(x), set_width(), set_tube_height());
                }
            ctx.drawImage(images.bottom, set_offset_x(), set_tube_offset_y(runs+1), set_width(), 75);


            var offset = set_tube_offset_y((tube/100) + 1) + 25;
            var counter = 0
            for(x=0;x<elements.length;x++) {

                switch (elements[x]) {
                    case 'probe':
                        element = images.probe;
                        height  = 20 * 1/6 * $('#myCanvas').height() / 100;
                        break;
                    case 'spacer10':
                        element = images.spacer10;
                        height  = 10 * 1/6 * $('#myCanvas').height() / 100;
                        break;
                    case 'spacer30':
                        element = images.spacer30;
                        height  = 30 * 1/6 * $('#myCanvas').height() / 100;
                        break;
                    case 'spacer80':
                        element = images.spacer80;
                        height  = 80 * 1/6 * $('#myCanvas').height() / 100;
                        break;
                }


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
        });
    }
    else {
        loadImages(sources, function(images) {
            ctx.drawImage(images.background, 0, 0, set_background_width(), set_background_height());
        });
    }
}

function set_background_size() {
    var w = $('#canvas-div').width();
    var h = $(window).height() * 0.8;
    $('#myCanvas').attr('width', w);
    $('#myCanvas').attr('height', h);
    var h2 = h + 8;
    $('#data-div').css('min-height', h2 + 'px');
}

function set_background_width() {
    var w = $('#myCanvas').width();
    return w;
}

function set_background_height() {
    var h = $('#myCanvas').height();
    return h;
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
