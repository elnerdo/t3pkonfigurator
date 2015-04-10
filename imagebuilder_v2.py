#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ImageBuilder(object):

    def __init__(self, configuration):
        self.configuration = configuration
        self.image_probe = '<img depth="{0}" class="img40" src="/t3pkonfigurator/static/probe.png">'
        self.image_spacer10 = '<img class="img20" width="20px"src="/t3pkonfigurator/static/spacer10.png">'
        self.image_spacer30 = '<img class="img60" width="20px" src="/t3pkonfigurator/static/spacer30.png">'
        self.image_spacer80 = '<img class="img160" width="20px"src="/t3pkonfigurator/static/spacer80.png">'
        self.css_class = self._set_class()

    def build_image(self):
        img_div = '<div id="{0}"><div class="{0}">{1}</div></div>'
        imagedict = {
            'probe': self.image_probe, 
            'spacer10': self.image_spacer10,
            'spacer30': self.image_spacer30,
            'spacer80': self.image_spacer80
        }
        counter = len(self.configuration['depths']) - 1

        testdict = {300: 'foobar',
            200: 'foobar2',
            100: 'foobar3',
            '': ''}

        testclass = testdict[self.configuration['tube']]
        images = '<div class="{0}">'.format(testclass)
        for i in reversed(self.configuration['order']):
            if i == 'probe':
                images += imagedict[i].format(self.configuration['depths'][counter])
                counter -= 1
            else:
                images += imagedict[i]
        images += '</div>'
        img = img_div.format(self.css_class, images)
        return img

    def build_canvas(self):

        imagedict = {
            'probe': ['16', '40'],
            'spacer10': ['16', '20'],
            'spacer30': ['16', '60'],
            'spacer80': ['16', '160']
        }

        offset = 0
        if self.configuration['tube'] == 300:
            offset = 0
        elif self.configuration['tube'] == 200:
            offset = 100
        elif self.configuration['tube'] == 100:
            offset = 180

        canvas_actions = 'var background = document.getElementById("tubeimg");\
ctx.drawImage(background, 0, {0}, 360, {1});'.format(offset, self.configuration['tube'] * 3)
        xval = 156
        try:
            yval = self.screw_this() - int(imagedict[self.configuration['order'][-1]][1])
        except:
            yval = 0
        var_counter = 0
        probe_counter = len(self.configuration['depths']) - 1
        for i in (self.configuration['order']):
            yval -= int(imagedict[i][1]) + 2
            if i == 'probe':
                canvas_actions += 'var img{0} = document.getElementById("img-{1}");\
ctx.drawImage(img{0}, {2}, {3}, {4}, {5});'.format(var_counter, i, xval, yval, imagedict[i][0], imagedict[i][1])
                probe_counter -= 1
            else:
                canvas_actions += 'var img{0} = document.getElementById("img-{1}");\
ctx.drawImage(img{0}, {2}, {3}, {4}, {5});'.format(var_counter, i, xval, yval, imagedict[i][0], imagedict[i][1])
            var_counter += 1

        js = "<script>$(document).ready(function() {var c = document.getElementById('myCanvas'); var ctx = c.getContext(\"2d\");"
        js += canvas_actions + "});</script>"
        return js

    def screw_this(self):
        if self.configuration['tube'] == 300:
            return 880
        elif self.configuration['tube'] == 200:
            return 700
        elif self.configuration['tube'] == 100:
            return 500

    def _set_class(self):
        imagedict = {
            300: 'image-div300',
            200: 'image-div200',
            100: 'image-div100',
            '': ''
        }
        return imagedict[self.configuration['tube']]
