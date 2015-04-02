#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm


class PDFGenerator(object):

    def __init__(self, data):
        self.configuration = data['configuration']
        self.tube = data['tube']
        self.offset = data['offset']
        self.summary = data['summary']
        self.filename = 't3p-config-' + str(time.clock()) + '.pdf'
        self.font = "Helvetica"
        self.font_bold = "Helvetica-Bold"

    def build(self):
        doc = SimpleDocTemplate(self.filename, 
	        rightMargin=1.5*cm, leftMargin=1.5*cm, topMargin=1.5*cm, bottomMargin=1.5*cm)

        story=[]

        # Add your logo to the page head. 
        #story.append(Image('logo.png', 2*cm, 2*cm))
         
        # Fetch the document stylesheet ...
        styles = getSampleStyleSheet()
        # ... and add the justify style.
        styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))

        # Add the document title to the content block.
        story.append(Paragraph('<font size=16>T3P-Konfiguration</font>', styles["Center"]))
        story.append(Spacer(0.1*cm, 0.5*cm))

        # To generate the content and write it to 
        # the *.pdf file (in this case firstDoc.pdf) 
        # just call the build method.
        doc.build(story)
        return self.filename
