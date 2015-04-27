#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ImageBuilder(object):

    def __init__(self):
        self.image_probe = '<img depth="{0}" class="img40" src="/t3pkonfigurator/static/probe.png">'
        self.image_spacer10 = '<img class="img20" width="20px"src="/t3pkonfigurator/static/spacer10.png">'
        self.image_spacer30 = '<img class="img60" width="20px" src="/t3pkonfigurator/static/spacer30.png">'
        self.image_spacer80 = '<img class="img160" width="20px"src="/t3pkonfigurator/static/spacer80.png">'
        self.canvas_actions = ''

    def build(self, elements, tube, depths):
        variables = "draw_canvas({0}, {1}, {2});".format(elements, tube, depths)
        return "<script>$('#background, #tubeimg-100, #tubeimg-top, #tubeimg-bottom').ready(function(){" + variables + "});</script>"
