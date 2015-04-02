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

    def build_imageWORKING(self):
        img_div = '<div class="{0}">{1}</div>'
        imagedict = {
            'probe': self.image_probe, 
            'spacer10': self.image_spacer10,
            'spacer30': self.image_spacer30,
            'spacer80': self.image_spacer80
        }
        images = '<div class="foobar">'
        for i in reversed(self.configuration['order']):
            images += imagedict[i]
        return img_div.format(self.css_class, images) + '</div>'

    def build_image(self):
        img_div = '<div id="{0}"><div class="{0}">{1}</div></div>'
        imagedict = {
            'probe': self.image_probe, 
            'spacer10': self.image_spacer10,
            'spacer30': self.image_spacer30,
            'spacer80': self.image_spacer80
        }
        counter = len(self.configuration['depths']) - 1
        images = '<div class="foobar">'
        for i in reversed(self.configuration['order']):
            if i == 'probe':
                images += imagedict[i].format(self.configuration['depths'][counter])
                counter -= 1
            else:
                images += imagedict[i]
        images += '</div>'
        img = img_div.format(self.css_class, images)
        return img

    def _set_class(self):
        imagedict = {
            300: 'image-div300',
            200: 'image-div200',
            100: 'image-div100'
        }
        return imagedict[self.configuration['tube']]
