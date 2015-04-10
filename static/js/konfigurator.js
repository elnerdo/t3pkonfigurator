$(document).ready(function() {
    $('.img40').each(function() {
        console.log($(this));
        var rect = this.getBoundingClientRect();
        console.log(rect.top, rect.right, rect.bottom, rect.left);
        var div = document.createElement('div');
        var text = document.createTextNode($(this).attr('depth') + 'cm');

        var screenWidth = window.screen.width;
        var screenHeight = window.screen.height;

        div.setAttribute('class', 'depthlegend');
        div.appendChild(text);

        var percentH = 100 * (rect.top + 15) / screenHeight;
        var percentW = 100 * (rect.left + 25) / screenWidth;

        console.log(screenHeight);
        
        var top = screenHeight * percentH / 100;
        var left = screenWidth * percentW / 100;

        $(div).css({'position': 'absolute',
                    'top': top,
                    'left': left});
        document.body.appendChild(div);
        
    });
});
