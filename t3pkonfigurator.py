#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import tornado.web
import tornado.escape
import tornado.httpclient
import tornado.httputil
import time
import os
from pdfgenerator import PDFGenerator
from formbuilder import FormBuilder
from configurationgenerator import ConfigurationGenerator
from imagebuilder import ImageBuilder
from messages import Messages

class MainHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.myrequests = ['deepest', 'add_probe', 'conf_done', 'prepare_submit',
            'depths', 'tube', 'offset', 'summary', 'configuration', 'cable',
            'amount', 'connector']
        self.request_dict = self._create_request_dict()
        self.messages = Messages()

    def _create_request_dict(self):
        rqdict = {}
        for x in self.myrequests:
            rqdict[x] = self.get_argument(x, '')
        return rqdict

    def get(self):
        fb = FormBuilder()
        html = fb.build_deepest()
        data = {}
        data['depths'] = []
        self.render('templates/main_v3.html',
                    msg=self.messages.initial_message,
                    html=html, data=data)

    def post(self):
        html = ''
        t3p = T3PKonfigurator(self.request_dict)
        data = t3p.handle_request()

        if 'html' in data:
            self.render('templates/main_v2.html',
                        msg=data['msg'],
                        html=data['html'],
                        img=data['img'])

        elif 'spezial' in data:
            pdfgen = PDFGenerator(data['spezial'])
            pdf = pdfgen.build()
            with open(pdf, 'r') as f:
                self.write(f.read())
            self.set_header("Content-Type", 'application/pdf; charset="utf-8"')
            self.set_header("Content-Disposition", "attachment; filename=" + pdf)
            os.remove(pdf)

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
        self.depths = []
        self.deepest = None
        self.messages = Messages()
        self.requestdata = data
        self.parts = self.get_parts()

    def handle_request(self):
        #data = None
        if self.requestdata['conf_done']:
            data = self.request_conf_done()
        elif self.requestdata['deepest']:
            data = self.request_deepest()
        elif self.requestdata['add_probe']:
            data = self.request_add_probe()
        elif self.requestdata['prepare_submit']:
            data = self.request_prepare_submit()
        return data

    def request_conf_done(self):
        self.depths = self.unicodestr_to_list(self.requestdata['conf_done'])
        cg = ConfigurationGenerator(self)
        configuration = cg.create_configuration()
        fb = FormBuilder()
        html = fb.build_conf_done(configuration)
        msg = self.messages.print_or_next
        ib = ImageBuilder(configuration)
        img = ib.build_image()
        return {'html': html, 'msg': msg, 'img': img}

    def request_deepest(self):
        if int(self.requestdata['deepest']) > self.maxdepth:
            msg = self.messages.too_deep_message
            html = ''
        else:
            self.deepest = int(self.requestdata['deepest'])
            self.depths.append(int(self.requestdata['deepest']))
            possible_depths = self.get_possible_depths()
            if possible_depths:
                msg = self.messages.add_probe_message
            else:
                msg = self.messages.max_elements_message
            fb = FormBuilder()
            html = fb.build_add(possible_depths, self.depths)
            cg = ConfigurationGenerator(self)
            configuration = cg.create_configuration()
            ib = ImageBuilder(configuration)
            img = ib.build_image()
        return {'html': html, 'msg': msg, 'img': img}

    def request_add_probe(self):
        depthlist = self.unicodestr_to_list(self.requestdata['depths'])
        for i in depthlist:
            self.depths.append(int(i))
        self.depths.append(int(self.requestdata['add_probe']))

        possible_depths = self.get_possible_depths()
        if possible_depths:
            msg = self.messages.add_probe_message
        else:
            msg = self.messages.max_elements_message
        fb = FormBuilder()
        html = fb.build_add(possible_depths, self.depths)
        cg = ConfigurationGenerator(self)
        configuration = cg.create_configuration()
        ib = ImageBuilder(configuration)
        img = ib.build_image()
        return {'html': html, 'msg': msg, 'img': img}   

    def request_prepare_submit(self):
        parts = self.calc_parts( self.unicodestr_to_list(self.requestdata['configuration']))
        pdfdata = self.prepare_pdfdata({
            'configuration': self.requestdata['configuration'],
            'tube': self.requestdata['tube'],
            'offset': self.requestdata['offset'],
            'summary': self.requestdata['summary'],
            'connector': self.requestdata['connector'],
            'cable': self.requestdata['cable'],
            'parts': parts,
            'amount': self.requestdata['amount']
        })
        return {'spezial': pdfdata}

    def get_possible_depths(self):
        possible_depths = []
        if not self.depths:
            return possible_depths
        i = 0
        while self.depths[-1] - self.probelength - (i * min(self.spacerlengths)) >= 10:
            possible_depths.append(self.depths[-1] - self.probelength - (i * min(self.spacerlengths)))
            i += 1
        return possible_depths

    def unicodestr_to_list(self, ustr):
        return ustr.strip('[] ').replace(' ', '').split(',')

    def prepare_pdfdata(self, formdata):
        summary = formdata['summary'].strip('</li>').split('</li><li>')
        formdata['summary'] = summary
        configuration = formdata['configuration'].strip('[] ').split(',')
        formdata['configuration'] = configuration
        return formdata

    def calc_parts(self, conf):
        keys = set(conf)
        parts = {}
        for key in keys:
            parts[key] = conf.count(key)
        return parts

    def get_parts(self):
        data = {'tubelengths': self.tubelengths,
         'reserved_space': self.reserved_space,
         'min_offset': self.min_offset,
         'max_offset': self.max_offset,
         'plug': self.plug,
         'probelength': self.probelength,
         'spacerlengths': self.spacerlengths,
        }
        return data
