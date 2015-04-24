#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import time

from reportlab.pdfgen import canvas
from reportlab.lib import utils
from reportlab.lib.units import cm


class PDFGenerator(object):

    def __init__(self, data):
        self.configuration = data.order
        self.tube = data.tube
        self.tubewidth = 30
        self.offset = data.offset
        self.summary = sorted(data.depths, key=lambda x: x)
        self.cable = data.cable
        self.connector = data.connector
        self.parts = data.parts
        self.amount = data.amount
        self.filename = 't3p-config-' + str(time.clock()) + '.pdf'
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


    def calc_image_relation(self, path, width=1*cm):
        # Keeps the height-width relation of the image.
        img = utils.ImageReader(path)
        iw, ih = img.getSize()
        aspect = ih / float(iw)
        dimensions = (width, width * aspect)
        return dimensions


    def build(self):
        c = canvas.Canvas(self.filename, pagesize=self.dina4)
        c.setLineWidth(0.7)
        self.draw_header(c)
        self.draw_heading(c)
        self.draw_tubehead(c)
        self.draw_tube(c)
        self.draw_tubebottom(c)
        self.draw_elements(c)
        self.draw_data(c)
        c.showPage()
        c.save()
        return self.filename

    def draw_header(self, canvas):
        headerheight = 100
        ypos = self.dina4[1] - headerheight
        canvas.drawImage('static/head.jpg', 0, ypos, width=self.dina4[0], height=headerheight)

    def draw_footer(self, canvas):
        footerwidth = self.dina4[0] - ( 2 * self.left )
        canvas.drawImage('static/footer.jpg', self.left, 25, width=footerwidth, height=100)

    def draw_heading(self, canvas):
        text = 'T3P-Konfiguration'
        canvas.setFont(self.font_bold, 14)
        canvas.drawString(210, 800, text)
        canvas.setFont(self.font, 12)

    def draw_tubehead(self, canvas):
        canvas.drawImage('static/PROFILE_top.png', self.left, 650, width=self.tubewidth, height=40, mask='auto')

    def draw_tube(self, canvas):
        ypos = 650 - self.tube*2
        canvas.drawImage('static/PROFILE_leer_100.png', self.left, ypos, width=self.tubewidth, height=self.tube*2, mask='auto')
        self.tubebottom = ypos

    def draw_tubebottom(self, canvas):
        ypos = self.tubebottom - 40
        canvas.drawImage('static/PROFILE_bottom.png', self.left, ypos, width=self.tubewidth, height=40, mask='auto')

    def draw_elements(self, canvas):
        imagedict = {
            'probe': {'image': 'static/probe.png', 'displayheight': 38, 'height': 20},
            'spacer10': {'image': 'static/spacer10.png', 'displayheight': 18, 'height': 10},
            'spacer30': {'image': 'static/spacer30.png', 'displayheight': 58, 'height': 30},
            'spacer80': {'image': 'static/spacer80.png', 'displayheight': 158, 'height': 80}
        }
        depthindex = len(self.summary) - 1
        y = self.tubebottom
        for i in (self.configuration):
            
            image = imagedict[i]['image']
            canvas.drawImage(image, self.leftelement, y,
                             width=20, height=imagedict[i]['displayheight'])
            self.add_length_legend(canvas, y + (imagedict[i]['displayheight']/3), imagedict[i]['height'])
            if i == 'probe':
                self.add_depth_legend(canvas, y + (imagedict[i]['displayheight']/2), self.summary[depthindex])
                depthindex -= 1
            
            y += 2
            y += imagedict[i]['displayheight']

    def draw_data(self, canvas):
        self.draw_intro_text(canvas)
        self.draw_summary(canvas)
        self.draw_tubelength(canvas)
        self.draw_tubeoffset(canvas)
        self.draw_cable(canvas)
        self.draw_connector(canvas)
        self.draw_amount(canvas)
        self.draw_parts(canvas)
        self.draw_todo_text(canvas)

    def draw_intro_text(self, canvas):
        txt = 'Durch die gewählten Messpunkte ergab sich folgende Konfiguration:'
        canvas.drawString(self.center, self.y, txt)
        self.y -= self.y_decrease

    def draw_todo_text(self, canvas):
        txt = 'PDF via Email an info@imko.de Betreff: T3P Konfiguration.'
        canvas.drawString(self.center, 100, txt)
        self.y -= self.y_decrease

    def draw_summary(self, canvas):
        canvas.drawString(self.center, self.y, 'Ihre Messpunkte:')
        self.y -= self.y_decrease
        for i in self.summary:
            text = "{0}. {1}cm".format(self.summary.index(i) + 1, i)
            canvas.drawString(self.center_indented, self.y, text)
            self.y -= self.y_decrease_small
        self.y -= 10


    def draw_parts(self, canvas):
        canvas.drawString(self.center, self.y, 'Verbaute Teile:')
        self.y -= self.y_decrease
        partsdict = {'probe': u'PICO-T3P',
         'spacer10': u'Platzhalter 10cm',
         'spacer30': u'Platzhalter 30cm',
         'spacer80': u'Platzhalter 80cm'}
        for i in sorted(self.parts):
            text = '{0} x {1}'.format(self.parts[i], partsdict[i])
            canvas.drawString(self.center_indented, self.y, text)
            self.y -= self.y_decrease

    def draw_tubelength(self, canvas):
        txt = 'Rohrlänge: {0}cm'.format(self.tube)
        canvas.drawString(self.center, self.y, txt)
        self.y -= self.y_decrease

    def draw_tubeoffset(self, canvas):
        txt = 'Rohrüberstand: {0}cm'.format(self.offset)
        canvas.drawString(self.center, self.y, txt)
        self.y -= self.y_decrease

    def draw_cable(self, canvas):
        txt = 'Kabellänge: {0}'.format(self.cable)
        canvas.drawString(self.center, self.y, txt)
        self.y -= self.y_decrease

    def draw_connector(self, canvas):
        txt = 'Anschluss: {0}'.format(self.connector)
        canvas.drawString(self.center, self.y, txt)
        self.y -= self.y_decrease

    def draw_amount(self, canvas):
        txt = 'Stückzahl: {0}'.format(self.amount)
        canvas.drawString(self.center, self.y, txt)
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
        canvas.drawString(self.depth_legend, y, str(text))
        canvas.restoreState()
