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
from cyglib.config import config
from cyglib import eps


class Component():

    def __init__(self, rack_order, item, seq, genomeloc, clip_start, clip_end, panel_height=0):

        self.rack_order = rack_order
        self.item = item
        self.seq = seq[clip_start-1:clip_end]
        self.genomeloc = genomeloc
        self.clip_start = clip_start
        self.clip_end = clip_end
        self.panel_height = panel_height

        self.call_message()

    def summary(self):

        summary = {self.__class__.__name__: self.rack_order}
        return summary


    def paragraph(self, coordinate, font, font_normal_size, indent=0):
        self.drawing = ''
        self.typography = ''


    def call_message(self):

        if isinstance(self.rack_order, (int, float)):
            print('Component: ' + self.__class__.__name__ + ' on rack #' + str(self.rack_order) + ' is built now.')

        else:
            print('Component: ' + self.__class__.__name__ + ' is built now.')


class Shaft(Component):

    def __init__(self, rack_order, item, seq, genomeloc, clip_start, clip_end, panel_height=0):
        super().__init__(rack_order, item, seq, genomeloc, clip_start, clip_end)
        self.item = self.item._replace(start=1)
        self.item = self.item._replace(end=len(self.seq))

    def paragraph(self, coordinate, font, font_normal_size, indent=0):
        super().paragraph(coordinate, font, font_normal_size, indent=0)

        x0 =  coordinate.x0
        x1 = coordinate.x1
        y = coordinate.y0

        self.drawing = \
            eps.comment('Shaft', indent=indent) + \
            eps.newpath(indent=indent) + \
            eps.mt(x0, y, indent=indent) + \
            eps.lt(x1, y, indent=indent) + \
            eps.stroke(indent=indent)


class Title(Component):

    def __init__(self, rack_order, item, seq, genomeloc, clip_start, clip_end, panel_height=0):
        super().__init__(rack_order, item, seq, genomeloc, clip_start, clip_end)
        self.item = self.item._replace(start=1)
        self.item = self.item._replace(position_spot=[1, (len(self.seq)-self.item.end)/2, len(self.seq)-self.item.end])

    def paragraph(self, coordinate, font, font_normal_size, indent=0):
        super().paragraph(coordinate, font, font_normal_size, indent=0)

        font_size = config.font_title_size
        tag = self.item.name
        if self.item.option=='left':
            x0 = coordinate.x0
            x1 = coordinate.x1 + len(tag) * font_size / 2
        elif self.item.option=='center':
            x0 = coordinate.x_spot[1]
            x1 = coordinate.x_spot[1] + (coordinate.x1 - coordinate.x0)
        else:
            x0 = coordinate.x_spot[2]
            x1 = coordinate.x_spot[2] + (coordinate.x1 - coordinate.x0) - len(tag) * font_size / 2
        y =  coordinate.y0
        coordinate_factor = config.title_height

        self.typography = \
            eps.comment('Title', indent=indent) + \
            eps.newpath(indent=indent) + \
            eps.center_txt((x0+x1)/2, y+coordinate_factor, tag, font, font_size, indent=indent) + \
            eps.stroke(indent=indent)


class ScaleBar(Component):

    def __init__(self, rack_order, item, seq, genomeloc, clip_start, clip_end, panel_height=0):
        super().__init__(rack_order, item, seq, genomeloc, clip_start, clip_end)

        new_item = self.item._replace(start=1)
        new_item = new_item._replace(position_spot=[1, (len(self.seq)-self.item.end)/2, len(self.seq)-self.item.end])
        self.item = new_item

    def paragraph(self, coordinate, font, font_normal_size, indent=0):
        super().paragraph(coordinate, font, font_normal_size, indent=0)

        if self.item.option=='left':
            x0 = coordinate.x0
            x1 = coordinate.x1
        elif self.item.option=='center':
            x0 = coordinate.x_spot[1]
            x1 = coordinate.x_spot[1] + (coordinate.x1 - coordinate.x0)
        else:
            x0 = coordinate.x_spot[2]
            x1 = coordinate.x_spot[2] + (coordinate.x1 - coordinate.x0)

        y =  coordinate.y0
        tag = format(self.item.end, ',d') + self.item.name if config.scale_bar_comma \
            else format(self.item.end, 'g') + self.item.name
        coordinate_factor = config.rack_interval*1/2

        self.drawing = \
            eps.newpath(indent=indent, line_width=config.ultra_bold_line) + \
            eps.mt(x0, y-coordinate_factor, indent=indent) + \
            eps.lt(x1, y-coordinate_factor, indent=indent) + \
            eps.stroke(indent=indent)

        self.typography = \
            eps.newpath(indent=indent) + \
            eps.center_txt((x0+x1)/2, y-2*coordinate_factor, tag, font, font_normal_size, indent=indent) + \
            eps.stroke(indent=indent)


class DashedLine(Component):
    def __init__(self, rack_order, item, seq, genomeloc, clip_start, clip_end, panel_height=0):
        super().__init__(rack_order, item, seq, genomeloc, clip_start, clip_end)
        self.item = self.item._replace(start=self.item.start-1)

    def paragraph(self, coordinate, font, font_normal_size, indent=0):
        super().paragraph(coordinate, font, font_normal_size, indent=0)
        self.drawing =  eps.newpath(indent=indent)\
                        + eps.mt(coordinate.x0, coordinate.y0, indent=indent)\
                        + eps.lt(coordinate.x1, coordinate.y0 + self.item.option * config.rack_interval, indent=indent)\
                        + '[1 2 3 2] 0 setdash\n'\
                        + eps.stroke(indent=indent)\
                        + '[] 0 setdash\n'                        