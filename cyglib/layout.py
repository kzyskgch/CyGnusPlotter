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
import types
from collections import Iterable
from cyglib.config import config
from cyglib import form


def new_layout(rack_interval=config.rack_interval,
                 side_margin=config.side_margin,
                 title_height=config.title_height):

    return Layout(rack_interval=rack_interval,
                 side_margin=side_margin,
                 title_height=title_height)


class Layout:

    def __init__(self,
                 rack_interval,
                 side_margin,
                 title_height):

        self.rack_interval = float(rack_interval)
        self.side_margin = float(side_margin)
        self.title_height = title_height

        self.length = 0
        self.width = 0
        self.output_width_without_margin = None
        self.scaling = 1

        self.component_group = list()

        self.rack_count = 0
        self.height = self.rack_interval * 3 + self.title_height

    def gets_component_group(self, new_component_group, add=None):

        if not add:
            self.component_group = list()

        if isinstance(new_component_group, Iterable):
            self.component_group.extend(new_component_group)
        else:
            self.component_group.append(new_component_group)

        self.length = max([len(i.seq) for i in self.component_group]+[self.length])
        self.width = self.length + self.side_margin * 2

        self.rack_count = max([i.rack_order for i in self.component_group if isinstance(i.rack_order, (int,float))] +[self.rack_count])
        self.height = (3 + self.rack_count)  * self.rack_interval

    def rescale(self, new_width_without_margin):
        self.output_width_without_margin = new_width_without_margin

    def coordinate(self, component):
        def coordinate_x(position):
            if isinstance(position, (int, float)):
                x = self.side_margin + (position * self.scaling)
            elif isinstance(position, (types.FunctionType, types.BuiltinFunctionType, types.BuiltinMethodType)):
                x = position()
            else:
                x = self.side_margin
            return x

        def coordinate_y(rack_order):
            if isinstance(rack_order, (int, float)):
                y = self.rack_interval * (rack_order + config.rack_margin)
            elif isinstance(rack_order, (types.FunctionType, types.BuiltinFunctionType, types.BuiltinMethodType, types.MethodType)):
                y = self.rack_interval * (rack_order() + config.rack_margin)
            else:
                y = self.rack_interval
            return y

        if self.output_width_without_margin:
            try:
                self.scaling = self.output_width_without_margin/self.length
                self.width = self.output_width_without_margin + self.side_margin * 2
            except:
                pass
        return form.new_coordinate(x0=coordinate_x(int(component.item.start) - 1),
                x1=coordinate_x(component.item.end),
                y0=coordinate_y(component.rack_order),
                x_spot=[coordinate_x(spot) for spot in component.item.position_spot])

    ###Rack_oder methods###
    def top(self):
        self.height = (3 + self.rack_count + sum([i.panel_height for i in self.component_group])) * self.rack_interval + self.title_height
        return self.rack_count + sum([i.panel_height for i in self.component_group])

    def upper(self):
        self.height = (3 + self.rack_count + sum([i.panel_height for i in self.component_group])) * self.rack_interval + self.title_height
        return  self.rack_count

    def bottom(self):
        return 0.5

    def direct(self, rack_order):
        def redirect():
            return rack_order
        return redirect

    def summary(self):
        summary = {'rack_interval':self.rack_interval,
                'side_margin': self.side_margin,
                'title_height': self.title_height,
                'scaling': self.scaling,
                'rack_count': self.rack_count
                }

        for i in self.component_group:
            summary.update(i.summary())
        return summary
