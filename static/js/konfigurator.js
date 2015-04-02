$(document).ready(function() {
    $('.img40').each(function() {
        console.log($(this));
        var rect = this.getBoundingClientRect();
        console.log(rect.top, rect.right, rect.bottom, rect.left);
        var div = document.createElement('div')
        var text = document.createTextNode($(this).attr('depth') + 'cm');
        
        div.appendChild(text);
        console.log($(div).text());
        $(div).css({'position': 'absolute',
                    'top': rect.top + 15,
                    'left': rect.left + 25});
        document.body.appendChild(div);
        
    });
});

function conf_done() {
        var conf_done = $('#depths').attr('value');
        $.ajax({
            type: "POST",
            url: "/t3pkonfigurator",
            data: { conf_done: conf_done}
        });
}


$(document).ready(function() {
    $('#deepest-btn').click(function() {
        var deepest = $('#deepest').attr('value');
        $.ajax({
            type: "POST",
            url: "/t3pkonfigurator",
            data: { deepest: deepest}
        });
    });
});

$(document).ready(function() {
    $('#add-btn').click(function() {
        var depths = $('#depths').attr('value');
        var add_probe = $('#add_probe').attr('value');
        $.ajax({
            type: "POST",
            url: "/t3pkonfigurator",
            data: { depths: depths, add_probe: add_probe}
        });
    });
});

function printDiv(divName) {
     //TODO: find a good way to handle the image problem...
     var baseurl = "http://localhost"
     $('#' + divName + ' img').each(function() {
        var src = $(this).attr('src');
        $(this).attr('src', baseurl + src);
     });
     var w = window.open();
     w.document.body.innerHTML = $('#' + divName).html();
     w.print();
     w.close();
}

function prepareSubmit() {
    var config = '';
    var tube = $('#tube').text();
    var offset = $('#offset').text();
    var summary = $('#summary').text();
    $('#config p').each(function() {
        config += (this.innerHTML) + ' ';
    });
    $.ajax({
        type: "POST",
        url: "/t3pkonfigurator",
        data: {configuration: config, tube: tube, offset: offset, summary: summary}
    }).done(function( data ) {
            $('#control-btns').css('visibility', 'hidden');
            $('#data-div').append(data.form);
    });
}

/*
function iframeLoaded() {
      var iFrameID = document.getElementById('idIframe');
      if(iFrameID) {
            // here you can make the height, I delete it first, then I make it again
            iFrameID.height = "";
            iFrameID.height = iFrameID.contentWindow.document.body.scrollHeight + "px";
      }   
  }*/
