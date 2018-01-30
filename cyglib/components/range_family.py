# -*- coding: utf-8 -*-
'''
Copyright 2018 Kazuya SAKAGUCHI Licensed under the
Educational Community License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may
obtain a copy of the License at

http://www.osedu.org/licenses/ECL-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS"
BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied. See the License for the specific language governing
permissions and limitations under the License.
'''
import math
import re

from cyglib.components.base import Component

from cyglib.config import config
from cyglib import eps


class Range(Component):

    def __init__(self, rack_order, item, seq, genomeloc, clip_start, clip_end, panel_height=0):
        super().__init__(rack_order, item, seq, genomeloc, clip_start, clip_end)

        if (item.start<clip_start and item.end<clip_start ) or (item.start>clip_end and item.end>clip_end):
            self.survive = False

        else:
            self.item = self.item._replace(start=self.item.start-clip_start+1, end=self.item.end-clip_start+1)
            self.survive = True


class Box(Range):

    def __init__(self, rack_order, item, seq, genomeloc, clip_start, clip_end, panel_height=0):
        super().__init__(rack_order, item, seq, genomeloc, clip_start, clip_end)
        self.size = config.box_size


    def paragraph(self, coordinate, font, font_normal_size, indent=0):
        super().paragraph(coordinate, font, font_normal_size, indent=0)

        tag = self.item.name
        x0 =  coordinate.x0
        x1 = coordinate.x1
        y = coordinate.y0
        s = self.size

        self.drawing = \
        self.survive * (
            eps.comment('Box', indent=indent) +
            eps.newpath(indent=indent) +
            eps.mt(x0, y - s, indent=indent) +
            eps.lt(x0, y + s, indent=indent) +
            eps.lt(x1, y + s, indent=indent) +
            eps.lt(x1, y - s, indent=indent) +
            eps.lt(x0, y - s, indent=indent) +
            eps.closepath(indent=indent) +
            eps.stroke(indent=indent)
            )

        self.typography = \
        self.survive * (
            eps.comment('Box', indent=indent) +
            eps.newpath(indent=indent) +
            eps.center_txt((x0+x1)/2, y, tag, font, font_normal_size, indent=indent) +
            eps.stroke(indent=indent)
            )


class Arrow(Range):

    def __init__(self, rack_order, item, seq, genomeloc, clip_start, clip_end, panel_height=0):
        super().__init__(rack_order, item, seq, genomeloc, clip_start, clip_end)

        self.shaft_size = config.shaft_size
        self.head_size = config.head_size


    def paragraph(self, coordinate, font, font_normal_size, indent=0):
        super().paragraph(coordinate, font, font_normal_size, indent=0)

        tag = self.item.name
        x0 =  coordinate.x0
        x1 = coordinate.x1
        y = coordinate.y0
        ss = self.shaft_size
        hs = self.head_size
        d = 0.5 * (x1 - x0)/math.fabs(x1 - x0) # direction

        self.drawing = \
            self.survive * (
            eps.comment('Arrow', indent=indent) +
            eps.newpath(indent=indent) +
            eps.mt(x0, y - ss, indent=indent) +
            eps.lt(x0, y + ss, indent=indent) +
            eps.lt(x1 - hs * d, y + ss, indent=indent) +
            eps.lt(x1 - hs * d, y + hs, indent=indent) +
            eps.lt(x1, y, indent) +
            eps.lt(x1 - hs * d, y - hs, indent=indent) +
            eps.lt(x1 - hs * d, y - ss, indent=indent) +
            eps.lt(x0,y - ss, indent=indent) +
            eps.closepath(indent=indent) +
            eps.stroke(indent=indent)
            )

        self.typography = \
            self.survive * (
            eps.comment('Arrow', indent=indent) +
            eps.newpath(indent=indent) +
            eps.center_txt((x0+x1)/2, y, tag, font, font_normal_size, indent=indent) +
            eps.stroke(indent=indent)
            )




class Probe(Range):
    def __init__(self, rack_order, item, seq, genomeloc, clip_start, clip_end, panel_height=0):
        super().__init__(rack_order, item, seq, genomeloc, clip_start, clip_end)


    def paragraph(self, coordinate, font, font_normal_size, indent=0):
        super().paragraph(coordinate, font, font_normal_size, indent=0)

        tag = self.item.name
        x0 =  coordinate.x0
        x1 = coordinate.x1
        y = coordinate.y0
        coordinate_factor = config.rack_interval*1/3

        self.drawing = \
            self.survive * (
            eps.comment('Probe', indent=indent) +
            eps.newpath(indent=indent, line_width=config.ultra_bold_line, colour='1 0.4 0') +
            eps.mt(x0, y, indent=indent) +
            eps.lt(x1, y, indent=indent) +
            #eps.closepath(indent=indent) +
            eps.stroke(indent=indent)
            )

        self.typography = \
            self.survive * (
            eps.comment('Probe', indent=indent) +
            eps.newpath(indent=indent, colour='0 0 0.9') +
            eps.center_txt((x0+x1)/2, y-coordinate_factor, tag, font, config.font_small_size, indent=indent) +
            eps.stroke(indent=indent)
            )


class MatchingProbe(Probe):
    def __init__(self, rack_order, item, seq, genomeloc, clip_start, clip_end, panel_height=0):
        super().__init__(rack_order, item, seq, genomeloc, clip_start, clip_end)

        new_spot = list()
        for i in range(len(seq)):
            string = seq[i:]
            if re.match('^' + self.item.pattern, string, re.I):
                new_spot.extend([i, i+len(self.item.pattern)])
        self.item = self.item._replace(position_spot=new_spot)


    def paragraph(self, coordinate, font, font_normal_size, indent=0):
        super().paragraph(coordinate, font, font_normal_size, indent=0)

        tag = self.item.name
        x = coordinate.x_spot
        y = coordinate.y0
        coordinate_factor = config.rack_interval*1/3

        for i in range(0, len(coordinate.x_spot), 2):
            self.drawing = self.drawing + \
                      eps.comment('MatchingProbe', indent=indent) + \
                      eps.newpath(indent=indent, line_width=config.ultra_bold_line, colour='1 0.4 0') +\
                      eps.mt(x[i], y, indent=indent) + \
                      eps.lt(x[i+1], y, indent=indent) + \
                      eps.stroke(indent=indent)

            self.typography = self.typography + \
                         eps.comment('MatchingProbe', indent=indent) + \
                         eps.newpath(indent=indent, colour='0 0 0.9') + \
                         eps.center_txt((x[i]+x[i+1])/2, y-coordinate_factor, tag, font, config.font_small_size, indent=indent) + \
                         eps.stroke(indent=indent)
                         

class Triangle(Range):
    def __init__(self, rack_order, item, seq, genomeloc, clip_start, clip_end, panel_height=0):
        super().__init__(rack_order, item, seq, genomeloc, clip_start, clip_end)

        self.half_size = config.triangle_half

    def paragraph(self, coordinate, font, font_normal_size, indent=0):
        super().paragraph(coordinate, font, font_normal_size, indent=0)

        label = self.item.name        
        x0 = coordinate.x0
        x1 = coordinate.x1
        y = coordinate.y0
        hs = self.half_size

        self.drawing = \
            self.survive * (
            eps.comment('Triangle', indent=indent) +
            eps.newpath(indent=indent) +
            eps.mt(x0, y - hs, indent=indent) +
            eps.lt(x0, y + hs, indent=indent) +
            eps.lt(x1, y, indent=indent) +
            eps.lt(x0, y - hs, indent=indent) +
            eps.closepath(indent=indent, colour='0 0 0') +
            eps.stroke(indent=indent)
            )

        self.typography = \
            self.survive * (
            eps.comment('Triangle', indent=indent) +
            eps.newpath(indent=indent) +
            eps.center_txt((x0+x1)/2, y+hs+config.font_small_size, label, font,  config.font_small_size, indent=indent) +
            eps.stroke(indent=indent)
            )


        
    
