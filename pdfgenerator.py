#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import uuid

from reportlab.pdfgen import canvas
from reportlab.lib import utils
from reportlab.lib.units import cm
from reportlab.lib.colors import Color, red
from reportlab.pdfbase.pdfmetrics import stringWidth


class PDFGenerator(object):

    def __init__(self, data, lang):
        self.lang = lang
        self.configuration = data.order
        self.tube = data.tube
        self.tubewidth = 30
        self.offset = data.offset
        self.summary = sorted(data.depths, key=lambda x: x)
        self.cable = data.cable
        self.connector = data.connector
        self.parts = data.parts
        self.amount = data.amount
        self.filename = 't3p-config-' + str(uuid.uuid4()) + '.pdf'
        self.font = "Helvetica"
        self.font_bold = "Helvetica-Bold"
        self.left = 50
        self.leftelement = 55
        self.center = 150
        self.center_indented = 175
        self.dina4 = (595, 842)
        self.y = 700
        self.y_decrease_small = 15
        self.y_decrease = 25
        self.length_legend = -85
        self.depth_legend = 15
        self.shrinkfactor = 0.8
        self.rect_offset_x = 10
        self.rect_offset_y = 10
        self.rect_width = 400
        self.rect_height = 25

    def calc_image_relation(self, path, width=1*cm):
        # Keeps the height-width relation of the image.
        img = utils.ImageReader(path)
        iw, ih = img.getSize()
        aspect = ih / float(iw)
        dimensions = (width, width * aspect)
        return dimensions

    def build(self):
        c = canvas.Canvas(self.filename, pagesize=self.dina4)
        c.setLineWidth(1.5)
        c.setFont(self.font_bold, 12)
        c.setFillColorCMYK(1, 0.5, 0.0, 0)
        c.setStrokeColorCMYK(1, 0.5, 0.0, 0)
        self.draw_header(c)
        self.draw_heading(c)
        self.draw_tubehead(c)
        self.draw_groundline(c)
        self.draw_tube(c)
        self.draw_tubebottom(c)
        self.draw_elements(c)
        self.draw_data(c)
        self.draw_footer(c)
        c.showPage()
        c.save()
        return self.filename

    def draw_header(self, canvas):
        headerheight = 100
        ypos = self.dina4[1] - headerheight
        canvas.drawImage(
            'static/head.jpg', 0, ypos, width=self.dina4[0],
            height=headerheight)

    def draw_footer(self, canvas):
        canvas.saveState()
        footerwidth = self.dina4[0] - (2 * self.left)
        canvas.setFillColorCMYK(1, 0.5, 0, 0)
        canvas.rect(0, 0, width=self.dina4[0], height=50, fill=True)
        canvas.setFillColorCMYK(0, 0, 0, 0)
        canvas.setFont(self.font_bold, 14)
        x = self.dina4[0]/2
        canvas.drawCentredString(x, 25, 'www.imko.de')
        canvas.linkURL('http://www.imko.de', (0, 50, self.dina4[1], 0))
        canvas.restoreState()

    def draw_heading(self, canvas):
        text = {'de': 'T3P-Konfiguration', 'en': 'T3P-Configuration'}
        canvas.saveState()
        canvas.setFont(self.font_bold, 14)
        canvas.setFillColorRGB(255, 255, 255)
        x = self.dina4[0]/2
        canvas.drawCentredString(x, 800, text[self.lang])
        canvas.restoreState()

    def draw_tubehead(self, canvas):
        self.add_depth_legend(canvas, 650, 0)
        self.add_length_legend(canvas, 650, self.offset)
        canvas.drawImage(
            'static/PROFILE_top.png', self.left, 650, width=self.tubewidth,
            height=40*self.shrinkfactor, mask='auto')

    def draw_groundline(self, canvas):
        ypos = 650
        canvas.line(10, ypos, 100, ypos)

    def draw_tube(self, canvas):
        ypos = 650 - self.tube * 2 * self.shrinkfactor
        canvas.drawImage(
            'static/PROFILE_leer_100.png', self.left, ypos,
            width=self.tubewidth, height=self.tube*2*self.shrinkfactor,
            mask='auto')
        self.tubebottom = ypos

    def draw_tubebottom(self, canvas):
        ypos = self.tubebottom - 40*self.shrinkfactor
        canvas.drawImage(
            'static/PROFILE_bottom.png', self.left, ypos,
            width=self.tubewidth, height=40*self.shrinkfactor, mask='auto')

    def draw_elements(self, canvas):
        imagedict = {
            'probe':
            {
                'image': 'static/probe.png',
                'displayheight': 38,
                'height': 20
            },
            'spacer10':
            {
                'image': 'static/spacer10.png',
                'displayheight': 18,
                'height': 10
            },
            'spacer30':
            {
                'image': 'static/spacer30.png',
                'displayheight': 58,
                'height': 30
            },
            'spacer80':
            {
                'image': 'static/spacer80.png',
                'displayheight': 158,
                'height': 80
            }
        }
        depthindex = len(self.summary) - 1
        y = self.tubebottom
        for i in (self.configuration):
            image = imagedict[i]['image']
            canvas.drawImage(
                image, self.leftelement, y, width=20,
                height=imagedict[i]['displayheight']*self.shrinkfactor)
            self.add_length_legend(
                canvas, y + (imagedict[i]['displayheight']/3),
                imagedict[i]['height'])
            if i == 'probe':
                self.add_depth_legend(
                    canvas, y + (imagedict[i]['displayheight']/2),
                    self.summary[depthindex])
                depthindex -= 1
            y += 2
            y += imagedict[i]['displayheight']*self.shrinkfactor

    def draw_data(self, canvas):
        self.draw_intro_text(canvas)
        self.draw_summary(canvas)
        self.y -= self.y_decrease_small
        self.draw_tubelength(canvas)
        self.y -= self.y_decrease_small
        self.draw_tubeoffset(canvas)
        self.y -= self.y_decrease_small
        self.draw_cable(canvas)
        self.y -= self.y_decrease_small
        self.draw_connector(canvas)
        self.y -= self.y_decrease_small
        self.draw_parts(canvas)
        self.y -= self.y_decrease_small
        self.draw_amount(canvas)
        self.y -= self.y_decrease_small
        self.draw_todo_text(canvas)

    def draw_intro_text(self, canvas):
        txt = {
            'de': 'Durch die gewählten Messpunkte ergab sich folgende \
Konfiguration:',
            'en': 'Given measuring points lead to the following \
configuration:'}
        canvas.drawString(self.center, self.y, txt[self.lang])
        self.y -= 2*self.y_decrease

    def draw_todo_text(self, canvas):
        txt = {
            'de': 'PDF via Email an info@imko.de Betreff: T3P Konfiguration.',
            'en': 'PDF via Email to info@imko.de Subject: T3P Configuration'}
        txt2 = {
            'de': 'Fügen Sie Ihre PICO-PROFILE T3PN Konfiguration der E-Mail \
bei.',
            'en': 'Attach your PICO-PROFILE T3PN configuration to the E-Mail.'
        }
        canvas.drawString(self.center, 100, txt[self.lang])
        canvas.drawString(self.center, 75, txt2[self.lang])
        canvas.rect(
            self._rect_x(self.center), self._rect_y(75),
            self.rect_width, self.rect_height*2)
        mailto = 'mailto:info@imko.de?subject=T3p-Konfiguration'
        canvas.linkURL(mailto, (self._rect_x(self.center), self._rect_y(75),
                       self._rect_x(self.center) + self.rect_width,
                       self._rect_y(75) + self.rect_height*2))
        canvas.line(248, 97, 330, 97)
        self.y -= self.y_decrease

    def draw_summary(self, canvas):
        txt = {'de': 'Ihre Messpunkte:', 'en': 'Your measuring points:'}
        canvas.drawString(self.center, self.y, txt[self.lang])
        self.y -= self.y_decrease

        for i in self.summary:
            text = "{0}. {1}cm".format(self.summary.index(i) + 1, i)
            canvas.drawString(self.center_indented, self.y, text)
            self.y -= self.y_decrease_small
        canvas.rect(
            self._rect_x(self.center),
            self._rect_y(self.y + self.y_decrease_small),
            self.rect_width,
            self.rect_height+(len(self.summary)*self.y_decrease_small)
            + self.y_decrease)
        self.y -= 10

    def draw_parts(self, canvas):
        txt = {'de': 'Verbaute Teile:', 'en': 'Installed parts:'}
        canvas.drawString(self.center, self.y, txt[self.lang])
        self.y -= self.y_decrease
        partsdict = {
            'probe': {'de': u'PICO-T3P', 'en': u'PICO-T3P'},
            'spacer10': {'de': u'Platzhalter 10cm', 'en': u'Spacer 10cm'},
            'spacer30': {'de': u'Platzhalter 30cm', 'en': u'Spacer 30cm'},
            'spacer80': {'de': u'Platzhalter 80cm', 'en': u'Spacer 80cm'}
        }
        for i in sorted(self.parts):
            text = '{0} x {1}'.format(self.parts[i], partsdict[i][self.lang])
            canvas.drawString(self.center_indented, self.y, text)
            self.y -= self.y_decrease
        canvas.rect(
            self._rect_x(self.center), self._rect_y(self.y + self.y_decrease),
            self.rect_width, self.rect_height*(len(self.parts)+1))

    def draw_tubelength(self, canvas):
        txt = {'de': 'Rohrlänge: {0}cm', 'en': 'Tubelength: {0}cm'}
        txt = txt[self.lang].format(self.tube)
        canvas.drawString(self.center, self.y, txt)
        canvas.rect(
            self._rect_x(self.center), self._rect_y(self.y), self.rect_width,
            self.rect_height)
        self.y -= self.y_decrease

    def draw_tubeoffset(self, canvas):
        txt = {'de': 'Rohrüberstand: {0}cm', 'en': 'Clearance: {0}cm'}
        txt = txt[self.lang].format(self.offset)
        canvas.drawString(self.center, self.y, txt)
        canvas.rect(
            self._rect_x(self.center), self._rect_y(self.y), self.rect_width,
            self.rect_height)
        self.y -= self.y_decrease

    def draw_cable(self, canvas):
        txt = {'de': 'Kabellänge: {0}', 'en': 'Cablelength: {0}'}
        txt = txt[self.lang].format(self.cable)
        canvas.drawString(self.center, self.y, txt)
        canvas.rect(
            self._rect_x(self.center), self._rect_y(self.y), self.rect_width,
            self.rect_height)
        self.y -= self.y_decrease

    def draw_connector(self, canvas):
        txt = {'de': 'Anschluss: {0}', 'en': 'Connector: {0}'}
        txt = txt[self.lang].format(self.connector)
        canvas.drawString(self.center, self.y, txt)
        canvas.rect(
            self._rect_x(self.center), self._rect_y(self.y), self.rect_width,
            self.rect_height)
        self.y -= self.y_decrease

    def draw_amount(self, canvas):
        txt = {'de': 'Stückzahl: {0}', 'en': 'Amount: {0}'}
        txt = txt[self.lang].format(self.amount)
        canvas.drawString(self.center, self.y, txt)
        canvas.rect(
            self._rect_x(self.center), self._rect_y(self.y), self.rect_width,
            self.rect_height)
        self.y -= self.y_decrease

    def add_length_legend(self, canvas, y, text):
        canvas.saveState()
        canvas.setFont(self.font, 10)
        canvas.rotate(90)
        canvas.drawString(y, self.length_legend, str(text))
        canvas.restoreState()

    def add_depth_legend(self, canvas, y, text):
        canvas.saveState()
        canvas.setFont(self.font, 10)
        canvas.drawString(self.depth_legend, y, str(text) + 'cm')
        canvas.restoreState()

    def _rect_x(self, x):
        return x - self.rect_offset_x

    def _rect_y(self, y):
        return y - self.rect_offset_y
