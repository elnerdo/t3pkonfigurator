#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ImageBuilder(object):

    def __init__(self):
        self.image_probe = '<img depth="{0}" class="img40" src="/t3pkonfigurator/static/probe.png">'
        self.image_spacer10 = '<img class="img20" width="20px"src="/t3pkonfigurator/static/spacer10.png">'
        self.image_spacer30 = '<img class="img60" width="20px" src="/t3pkonfigurator/static/spacer30.png">'
        self.image_spacer80 = '<img class="img160" width="20px"src="/t3pkonfigurator/static/spacer80.png">'
        self.canvas_actions = ''

    def build(self):
        return "<script>$(document).ready(function(){" + self.canvas_actions + "});</script>"

    def set_background(self):
        self.canvas_actions += "set_background();"

    def set_tube(self, tube):
        self.canvas_actions += "set_tubehead();set_tube({0});".format(tube)

    def set_elements(self, elements, tube, depths):
        self.canvas_actions += "set_elements({0}, {1}, {2});".format(elements, tube, depths)

    def build_canvas(self, configuration):
        self.configuration = configuration
        imagedict = {
            'probe': ['16', '40'],
            'spacer10': ['16', '20'],
            'spacer30': ['16', '60'],
            'spacer80': ['16', '160']
        }

        #js = self.set_background()
        js = self.draw_tube()

        return js


    def draw_element(self, index, id, x, y, width, height):
        js = 'var img{index} = document.getElementById("img-{id}");\
ctx.drawImage(img{index}, {x}, {y}, {width}, {height});'
        return js.format(index=index, id=id, x=x, y=y, width=width, height=height)
