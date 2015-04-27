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
from configurationgenerator import ConfigurationGenerator
from imagebuilder import ImageBuilder
from messages import MessagesDE, MessagesEN


class MainHandler(tornado.web.RequestHandler):

    def initialize(self, lang="de"):
        self.lang = lang
        self.templates = {"de": "templates/main_de.html",
                          "en": "templates/main_en.html"}
        self.myrequests = ['add_probe', 'rm_probe', 'probes_done', 'depths', 'create_pdf',
                           'amount', 'cable', 'connector']
        self.request_dict = self._create_request_dict()
        if self.lang == "de":
            self.messages = MessagesDE()
        elif self.lang == "en":
            self.messages = MessagesEN()
        else: #should never happen
            self.messages = MessagesEN()

    def _create_request_dict(self):
        rqdict = {}
        for x in self.myrequests:
            rqdict[x] = self.get_argument(x, '')
        return rqdict

    def get(self):
        data = T3PKonfigurator(self.request_dict)
        data.create_configuration()
        conf = {'tube': data.configuration.tube,
                'depths': data.configuration.depths,
                'order': data.configuration.order}
        ib = ImageBuilder()
        img = ib.build(conf['order'], conf['tube'], conf['depths'])
        
        self.render(self.templates[self.lang],
                    msg=self.messages.initial_message,
                    data=data, img=img)

    def post(self):
        print self.request_dict
        data = T3PKonfigurator(self.request_dict)
        data.create_configuration()
        conf = {'tube': data.configuration.tube,
                'depths': data.configuration.depths,
                'order': data.configuration.order}

        ib = ImageBuilder()
        img = ib.build(conf['order'], conf['tube'], conf['depths'])

        if self.request_dict['probes_done']:
            data.probes_done = True

        if self.request_dict['create_pdf']:
            data.create_configuration()
            pdf = data.create_pdf()
            with open(pdf, 'r') as f:
                self.write(f.read())
                self.set_header("Content-Type", 'application/pdf; charset="utf-8"')
                self.set_header("Content-Disposition", "attachment; filename=" + pdf)
            os.remove(pdf)

        msg = self.set_message(data)

        self.render(self.templates[self.lang], msg=msg, data=data, img=img)

    def set_message(self, data):
        if self.request_dict['add_probe'] or self.request_dict['rm_probe']:
            if data.possible_depths:
                return self.messages.add_probe_message
            elif not data.possible_depths and not data.depths:
                return self.messages.initial_message
            else:
                return self.messages.max_elements_message
        else:
            return self.messages.finish


class T3PKonfigurator(object):

    def __init__(self, data):
        self.tubelengths = [300, 200, 100]
        self.plug = 10
        self.min_offset = 10
        self.max_offset = 30
        self.reserved_space = self.plug + self.min_offset
        self.probelength = 20
        self.spacerlengths = [80, 30, 10]
        self.maxdepth = max(self.tubelengths) - self.reserved_space - (self.probelength / 2)
        self.depths = self.get_depths(data)
        self.possible_depths = self.get_possible_depths(data)
        self.finished = self.finish(data)
        self.amount = data['amount']
        self.cable = data['cable']
        self.connector = data['connector']
        self.probes_done = False


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
