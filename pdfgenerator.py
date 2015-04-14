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
        self.offset = data.offset
        self.summary = sorted(data.depths, key=lambda x: x)#(len(x), x[0], x[1], x[2]))
        self.cable = data.cable
        self.connector = data.connector
        self.parts = data.parts
        self.amount = data.amount
        self.filename = 't3p-config-' + str(time.clock()) + '.pdf'
        self.font = "Helvetica"
        self.font_bold = "Helvetica-Bold"
        self.left = 50
        self.center = 150
        self.center_indented = 175
        self.dina4 = (595, 842)
        self.y = 800
        self.y_decrease_small = 15
        self.y_decrease = 25
        self.length_legend = -85
        self.depth_legend = 15
        print data


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
        #c.setFillColorRGB(0,0,0.77)
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        
        self.draw_heading(c)
        self.draw_intro_text(c)
        self.draw_summary(c)
        self.draw_tube(c)
        self.draw_offset(c)
        #self.draw_configuration(c)
        self.draw_parts(c)
        self.draw_connector_and_cable(c)
        self.draw_amount(c)
        self.draw_image_dummy(c)
        # Close the PDF object cleanly, and we're done.
        c.showPage()
        c.save()
        return self.filename

    def draw_heading(self, canvas):
        text = 'T3P-Konfiguration'
        canvas.setFont(self.font_bold, 14)
        canvas.drawString(210, self.y, text)
        self.y -= self.y_decrease
        canvas.setFont(self.font, 12)

    def draw_intro_text(self, canvas):
        text = 'Die von ihnen angegebenen Informationen ergeben folgende Konfi\
guration:'
        canvas.drawString(self.center, self.y, text)
        self.y -= self.y_decrease

    def draw_summary(self, canvas):
        canvas.drawString(self.center, self.y, 'Ihre Messpunkte:')
        self.y -= self.y_decrease
        for i in self.summary:
            text = "{0}. {1}".format(self.summary.index(i) + 1, i)
            canvas.drawString(self.center_indented, self.y, text)
            self.y -= self.y_decrease_small
        self.y -= 10

    def draw_tube(self, canvas):
        text = u'Rohrlänge: ' + str(self.tube) + 'cm'
        canvas.drawString(self.center, self.y, text)
        self.y -= self.y_decrease

    def draw_offset(self, canvas):
        text = u'Rohrüberstand: ' + str(self.offset) + 'cm'
        canvas.drawString(self.center, self.y, text)
        self.y -= self.y_decrease

    def draw_configuration(self, canvas):
        for i in self.configuration:
            canvas.drawString(self.center, self.y, i)
            self.y -= self.y_decrease

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

    def draw_connector_and_cable(self, canvas):
        text = "Anschluss: {0}".format(self.connector)
        canvas.drawString(self.center, self.y, text)
        self.y -= self.y_decrease
        text = "Kabellänge: {0}".format(self.cable)
        canvas.drawString(self.center, self.y, text)
        self.y -= self.y_decrease

    def draw_amount(self, canvas):
        text = u'Stückzahl: {0}'.format(self.amount)
        canvas.drawString(self.center, self.y, text)
        self.y -= self.y_decrease

    def draw_image_dummy(self, canvas):
        imagedict = {
            'probe': {'image': 'static/probe.png', 'displayheight': 40, 'height': 20},
            'spacer10': {'image': 'static/spacer10.png', 'displayheight': 20, 'height': 10},
            'spacer30': {'image': 'static/spacer30.png', 'displayheight': 60, 'height': 30},
            'spacer80': {'image': 'static/spacer80.png', 'displayheight': 160, 'height': 80}
        }

        canvas.drawImage('static/empty.png', self.left, 752, width=20, height=40)
        self.add_length_legend(canvas, 752, self.offset)
        canvas.drawImage('static/empty.png', self.left, 710, width=20, height=40)
        if (int(self.summary[0])) - 10 > 0:
            self.add_length_legend(canvas, 710 + (40/3), str(int(self.summary[0])-10))
            y = 710
        else:
            y = 750
        canvas.line(10, 750, 100, 750)
        depthindex = 0
        for i in reversed(self.configuration):
            y -= imagedict[i]['displayheight']
            image = imagedict[i]['image']
            canvas.drawImage(image, self.left, y,
                             width=20, height=imagedict[i]['displayheight'])
            self.add_length_legend(canvas, y + (imagedict[i]['displayheight']/3), imagedict[i]['height'])
            if i == u"'probe'":
                self.add_depth_legend(canvas, y + (imagedict[i]['displayheight']/2), self.summary[depthindex])
                depthindex += 1
            y -= 2
            canvas.drawImage('static/seperator.png', self.left, y, width=20, height=2) 
            
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
