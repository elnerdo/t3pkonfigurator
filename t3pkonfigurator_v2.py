#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import tornado.web
import tornado.escape
import tornado.httpclient
import tornado.httputil
import time
import os
import ast
from pdfgenerator import PDFGenerator
from configurationgenerator_v2 import ConfigurationGenerator
from imagebuilder_v2 import ImageBuilder
from messages import Messages


class TestHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('templates/test.html')


class MainHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.myrequests = ['add_probe', 'rm_probe', 'probes_done', 'depths', 'create_pdf',
                           'amount', 'cable', 'connector']
        self.request_dict = self._create_request_dict()
        self.messages = Messages()

    def _create_request_dict(self):
        rqdict = {}
        for x in self.myrequests:
            rqdict[x] = self.get_argument(x, '')
        return rqdict

    def get(self):
        data = T3PKonfigurator(self.request_dict)
        self.render('templates/main_v3.html',
                    msg=self.messages.initial_message,
                    data=data, img='')

    def post(self):
        data = T3PKonfigurator(self.request_dict)
        data.create_configuration()

        conf = {'tube': data.configuration.tube,
                'depths': data.configuration.depths,
                'order': data.configuration.order}

        ib = ImageBuilder(conf)
        img = ib.build_canvas()#build_image()

        if self.request_dict['create_pdf']:
            data.create_configuration()
            pdf = data.create_pdf()
            with open(pdf, 'r') as f:
                self.write(f.read())
                self.set_header("Content-Type", 'application/pdf; charset="utf-8"')
                self.set_header("Content-Disposition", "attachment; filename=" + pdf)
            os.remove(pdf)
        self.render('templates/main_v3.html', msg=None, data=data, img=img)


class T3PKonfigurator(object):

    def __init__(self, data):
        self.tubelengths = [300, 200, 100]
        self.plug = 10
        self.min_offset = 15
        self.max_offset = 30
        self.reserved_space = self.plug + self.min_offset
        self.probelength = 20
        self.spacerlengths = [80, 30, 10]
        self.maxdepth = max(self.tubelengths) - self.reserved_space - (self.probelength / 2)
        self.depths = self.get_depths(data)
        self.possible_depths = self.get_possible_depths(data)
        self.finished = self.finish(data)
        self.messages = Messages()
        self.amount = data['amount']
        self.cable = data['cable']
        self.connector = data['connector']

    def finish(self, data):
        if data['probes_done']:          
            self.depths = [ item.encode('ascii') for item in ast.literal_eval(data['probes_done']) ]
            return True
        return False


    def create_configuration(self):
        cg = ConfigurationGenerator(self)
        self.configuration = cg.create_configuration()


    def create_pdf(self):
        self.configuration.amount = self.amount
        self.configuration.cable = self.cable
        self.configuration.connector = self.connector
        parts = self.calc_parts( self.configuration.order)
        pdfgen = PDFGenerator(self.configuration)
        pdf = pdfgen.build()
        return pdf

    def get_depths(self, data):
        if not data['depths']:
            depths = []
        else:
            depths = [ item.encode('ascii') for item in ast.literal_eval(data['depths']) ]
        if data['add_probe']:
            depths.append(data['add_probe'].encode('ascii'))
        if data['rm_probe']:
            del depths[-1]
        return depths


    def get_possible_depths(self, data):
        possible_depths = []
        if not len(self.depths):
            return possible_depths
        i = 0
        while int(self.depths[-1]) - self.probelength - (i * min(self.spacerlengths)) >= 10:
            possible_depths.append(int(self.depths[-1]) - self.probelength - (i * min(self.spacerlengths)))
            i += 1
        return possible_depths

    def calc_parts(self, conf):
        keys = set(conf)
        parts = {}
        for key in keys:
            parts[key] = conf.count(key)
        return parts
