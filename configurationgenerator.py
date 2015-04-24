#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ConfigurationGenerator(object):

    def __init__(self, t3p):
        self.depths = [int(i) for i in t3p.depths]
        self.tubelengths = t3p.tubelengths
        self.reserved_space = t3p.reserved_space
        self.min_offset = t3p.min_offset
        self.max_offset = t3p.max_offset
        self.plug = t3p.plug
        self.probelength = t3p.probelength
        self.spacerlengths = t3p.spacerlengths
        self.spaces = []
        self.spacers = []
        self.tube = ''
        self.order = []
        self.totalspaceused = ''
        self.offset = ''
        self.parts = ''

    def create_configuration(self):
        if not self.depths:
            return self
        self.tube = self.calc_tube()
        self.spaces = self.calc_spaces()
        self.spacers = self.calc_spacers()
        self.order = self.calc_order()       
        self.totalspaceused = self.calc_total_space_used()
        self.check_extra_spacers_bottom()
        self.parts = self.calc_parts()
        conf = {'tube': self.tube, 'order': self.order, 'offset': self.offset,
                'depths': self.depths, 'parts': self.parts}
        return self

    def calc_tube(self):
        i = 0
        if not len(self.depths):
            return 0
        while self.tubelengths[i] - int(max(self.depths)) - self.plug - (self.probelength / 2) >= self.min_offset: 
            tube = self.tubelengths[i]
            if i == len(self.tubelengths) - 1:
                break
            i += 1
        return tube

    def calc_spaces(self):
        i = 1
        spaces = []
        limit = len(self.depths) - 1
        while i <= limit:
            spaces.append(int(self.depths[i - 1]) - int(self.depths[i]))
            i += 1
        return spaces

    def calc_spacers(self):
        spacers = []
        for i in self.spaces:
            spacers.append(self.calc_spacers_needed(i))
        return spacers

    def calc_order(self):
        order = ['probe']
        for i in self.spacers:
            if not i:
                order.append('probe')
            else:
                for j in i:
                    order.append('spacer{0}'.format(j))
                order.append('probe')
        return order

    def calc_parts(self):
        keys = set(self.order)
        parts = {}
        for key in keys:
            parts[key] = self.order.count(key)
        return parts

    def check_extra_spacers_bottom(self):
        freespace = self.tube - self.totalspaceused
        currentoffset = freespace - int(min(self.depths) - (self.probelength / 2))
        i = 0
        while currentoffset > self.max_offset:
            if currentoffset - self.spacerlengths[i] >= self.min_offset:
                currentoffset -= self.spacerlengths[i]
                spacer = 'spacer{0}'.format(self.spacerlengths[i])
                self.order.insert(0,spacer)
            else:
                i += 1
        self.offset = currentoffset

    def spacer_probe_order(self):
        for i in self.spaces:
            self.spacers.append(self.calc_spacers_needed(i))

    def calc_spacers_needed(self, space):
        spacers = []
        rest = space - self.probelength
        i = 0
        while rest > 0:
            if rest - self.spacerlengths[i] >= 0:
                rest -= self.spacerlengths[i]
                spacers.append(self.spacerlengths[i])
            else:
                i += 1
        return spacers

    def calc_total_space_used(self):
        totalspaceused = self.plug
        switchcasetable = {
            'spacer10': 10,
            'spacer30': 30,
            'spacer80': 80,
            'probe': 20
        }
        for i in self.order:
            totalspaceused += switchcasetable[i]
        return totalspaceused
