#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ImageBuilder(object):

    def build(self, elems, tube, depths):
        variables = "draw_canvas({0}, {1}, {2});".format(elems, tube, depths)
        script_start = "<script>$('#background, #tubeimg-100, #tubeimg-top,\
                       #tubeimg-bottom').ready(function(){"
        script_end = "});</script>"
        script = script_start + variables + script_end
        return script
