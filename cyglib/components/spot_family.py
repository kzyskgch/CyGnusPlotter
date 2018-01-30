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
import re
import math

from cyglib.components.base import Shaft

from cyglib.config import config
from cyglib import eps
from cyglib import dbclient
from cyglib import local_data_access


class Spot(Shaft):
    pass


class Site(Spot):

    def __init__(self, rack_order, item, seq, genomeloc, clip_start, clip_end, panel_height=0):
        super().__init__(rack_order, item, seq, genomeloc, clip_start, clip_end)
        new_spot = list()#[i.start() + self.item.position_on_pattern for i in re.finditer(self.item.pattern, self.seq, re.I)]
        for i in range(len(seq)):
            string = self.seq[i:]
            if re.match('^'+self.item.pattern, string, re.I):
                new_spot.append(i+self.item.position_on_pattern)
        self.item = self.item._replace(position_spot=new_spot)

    def paragraph(self, coordinate, font, font_normal_size, indent=0):
        half_size = font_normal_size/2

        tag = self.item.name
        x0 = coordinate.x0
        y = coordinate.y0

        self.drawing = \
            eps.comment('Site', indent=indent) + \
            eps.newpath(indent=indent) + \
            ''.join([eps.mt(i, y + config.half_site_width, indent=indent+4) + eps.lt(i, y - config.half_site_width, indent=indent+4) for i in coordinate.x_spot]) + \
            eps.stroke(indent=indent)

        self.typography = \
            eps.comment('Site', indent=indent) + \
            eps.newpath(indent=indent) + \
            eps.right_txt(x0-half_size, y, tag, font, font_normal_size, indent=indent) + \
            eps.stroke(indent=indent)


class OuterBoxNum(Spot):

    def __init__(self, rack_order, item, seq, genomeloc, clip_start, clip_end, panel_height=0):
        super().__init__(rack_order, item, seq, genomeloc, clip_start, clip_end)

        self.item = self.item._replace(end=len(self.seq))


    def paragraph(self, coordinate, font, font_normal_size, indent=0):
        three_quarters_size = font_normal_size*3/4

        num_group = self.item.name
        self.num_boxes = len(coordinate.x_spot)

        box_x = coordinate.x_spot

        y = coordinate.y0

        self.drawing = ''

        self.typography =  \
            eps.comment('OuterBoxNum', indent=indent) + \
            eps.newpath(indent=indent)

        current_x = 0
        for i in range(0, self.num_boxes):
            min_interval = three_quarters_size * len(num_group[i])
            x_interval = box_x[i] - current_x

            if x_interval < min_interval and box_x[i-1] == current_x and (box_x[min(i+1, len(box_x)-1)]-box_x[i]>min_interval*2 or i==(len(box_x)-1)):

                new_x = current_x + min_interval

            elif x_interval < min_interval:
                new_x = current_x
                num_group[i] = ''

            else:
                new_x = box_x[i]

            current_x = new_x

            self.typography = self.typography + \
                eps.center_txt(current_x, y  - config.box_size - config.font_normal_size + config.font_normal_size/3,
                               num_group[i], font, config.font_normal_size, indent+4) +\
                eps.stroke(indent=indent+4)


class SNP(Spot):

    def __init__(self, rack_order, item, seq, genomeloc, clip_start, clip_end, panel_height=0):
        super().__init__(rack_order, item, seq, genomeloc, clip_start, clip_end)

        self.snp_search = dbclient.EnsemblClientForSNP(probe_id_group = self.item.name, genomeloc = self.genomeloc)
        #new_spot = self.snp_search.found_position
        self.num_hit = len(self.snp_search.found_position)

        result_inv = {self.snp_search.found_position[i]:self.snp_search.found_name[i] for i in range(self.num_hit)}
        new_spot = self.snp_search.found_position[:]
        new_spot.sort()
        self.found_names = [result_inv[i] for i in new_spot]

        self.item = self.item._replace(position_spot=new_spot)


    def paragraph(self, coordinate, font, font_normal_size, indent=0):
        x = coordinate.x_spot
        three_quarters_size = config.font_small_size*3/4
        minimum_interval = three_quarters_size * (config.probe_name_length-3)

        txt_x = list()
        for i in range(0, self.num_hit):
            if i < 3 or x[i] >= (x[i-3] + minimum_interval):
                txt_x.append(x[i])
            else:
                txt_x.append(x[i-3] + minimum_interval)

        y = coordinate.y0
        height_coordinate = [y + (3*config.font_small_size-2) - (i*config.font_small_size) for i in range(1, 4) ] * (self.num_hit)

        self.drawing = \
            eps.comment('SNP', indent=indent) + \
            eps.newpath(indent=indent, colour='1 0.4 0', line_width=config.bold_line) + \
            (''.join([eps.mt(i+config.cross_size, y + config.cross_size+config.rack_interval, indent=indent+4) + eps.lt(i-config.cross_size, y - config.cross_size+config.rack_interval, indent=indent+4) +
            eps.mt(i-config.cross_size, y + config.cross_size + config.rack_interval, indent=indent+4) + eps.lt(i+config.cross_size, y - config.cross_size+config.rack_interval, indent=indent+4) for i in coordinate.x_spot]) +
            eps.stroke(indent=indent)
         )

        self.typography = \
            eps.comment('SNP', indent=indent) + \
            eps.newpath(indent=indent, colour='0 0 0.9') + \
            ''.join([eps.center_txt(txt_x[i], height_coordinate[i], self.found_names[i], font, config.font_small_size, indent+4)  for i in  range(0, self.num_hit)]) + \
            eps.stroke(indent=indent)



class InfMet(Spot):

    def __init__(self, rack_order, item, seq, genomeloc, clip_start, clip_end, panel_height=0):
        super().__init__(rack_order, item, seq, genomeloc, clip_start, clip_end)
        #item.option is occupied to specify a platform. KS considers it is better that make it changeable by option.
        #It is a most easy method to do it, option is changed to
        self.height_probe_name = config.height_probe_name

        self.item = self.item._replace(end=len(self.seq))

        self.result = local_data_access.InfMetAccess(self.item.name, self.genomeloc, self.item.option).result
        self.num_hit  = len(self.result)
        result_inv = {v:k for k, v in self.result.items()}

        new_spot = [i for i in self.result.values()]
        new_spot.sort()

        self.hit_id = [result_inv[i] for i in sorted(result_inv.keys())]
        self.item = self.item._replace(position_spot=new_spot)

        if self.num_hit==0:
            pass
        else:
            factor =  config.font_small_size / config.rack_interval / config.num_probes_in_one_line
            self.panel_height = self.height_probe_name + self.panel_height + (self.num_hit*factor)

    def paragraph(self, coordinate, font, font_normal_size, indent=0):

        x = coordinate.x_spot
        x0 = coordinate.x0

        xdiv = (coordinate.x1-config.probe_name_length*config.font_small_size)/(self.num_hit+1)
        txt_x = [x0+xdiv*(i+1)
                - config.probe_name_length
                * config.font_small_size
                / 2 #half of probe name length
                 for i in range(0, self.num_hit)]
        line_terminal_x = [x0+xdiv*(i+1)
                        + config.probe_name_length
                        * config.font_small_size
                        * (i/self.num_hit - 1 )
                        / 2 #half of probe name length
                for i in range(0, self.num_hit)]

        y = coordinate.y0
        ydiv = config.num_probes_in_one_line
        unit = math.floor(self.num_hit/ydiv) + 1

        height_coordinate = [(y+config.rack_interval*self.height_probe_name)
                            + (i*config.font_small_size) for i in list(range(unit, 0, -1)) ] * 9 #nine is repeat.
        txt_y = [height_coordinate[i] for i in range(0, self.num_hit)]
        line_terminal_y = [height_coordinate[i] for i in range(0, self.num_hit)]

        self.drawing = \
            eps.comment('InfMet', indent=indent) + \
            eps.newpath(indent=indent, colour='1 0.4 0', line_width=config.bold_line) + \
            ''.join([
                eps.mt(line_terminal_x[i], line_terminal_y[i], indent=indent+4) +
                eps.lt(x[i], y  + config.box_size, indent=indent+4) +
                eps.lt(x[i], y - config.half_site_width, indent=indent+4)
                for i in range(0, self.num_hit)]) + \
            eps.stroke(indent=indent)
        self.typography = \
            eps.comment('InfMet', indent=indent) + \
            eps.newpath(indent=indent, colour='0 0 0.9') + \
            ''.join([
                eps.show_txt(txt_x[i], txt_y[i], self.hit_id[i], font, config.font_small_size, indent+4)
                for i in range(0, self.num_hit)]) + \
            eps.stroke(indent=indent)

    def summary(self):

        summary = super().summary()
        summary.update({'SeachInfMet # of hit':self.num_hit})
        summary.update(self.result)

        return summary
