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


def new_eps(layout, line_width=config.line_width,
          font=config.font, font_normal_size=config.font_normal_size):

    return EPS(layout, line_width=line_width, font=font, font_normal_size=font_normal_size)


class EPS:
    def __init__(self, layout, line_width, font, font_normal_size):
        self.layout = layout
        self.line_width = line_width
        self.font = font
        self.font_normal_size = font_normal_size
        self.script = ''

    def gets_component_group(self, component_group, add=None):
        self.layout.gets_component_group(component_group, add=None)
        paragraph_collection = self.collects_paragraphs()
        if not add:
            self.script = '%!PS-Adobe-3.0 EPSF-3.0\n'\
                        '%%BoundingBox: 0 0 ' + str(int(self.layout.width))\
                        + ' ' + str(int(self.layout.height))\
                        + '\n' + '%%HiResBoundingBox: 0 0 '\
                        + round_str(self.layout.width) + ' '\
                        + round_str(self.layout.height)\
                        + '\n\n' + round_str(self.line_width) + ' setlinewidth\n\n'\
                        + '/' + self.font + ' findfont '\
                        + round_str(self.font_normal_size)\
                        +  ' scalefont setfont\n' \
                        '/centershow\n'\
                        '{dup stringwidth pop\n'\
                        '2 div neg\n'\
                        '0 rmoveto\n'\
                        'show} def\n\n'\
                        '/rightshow\n'\
                        '{dup stringwidth pop\n'\
                        'neg\n'\
                        '0 rmoveto\n'\
                        'show} def\n\n'
        self.script = self.script + paragraph_collection

    def collects_paragraphs(self):
        self.drawing = str()
        self.typography = str()
        for component in self.layout.component_group:
            component.paragraph(self.layout.coordinate(component), self.font,
                                self.font_normal_size)
            self.drawing = self.drawing + component.drawing
            self.typography = self.typography + component.typography
        return self.drawing + self.typography

    def save(self, file_path=None):
        header = '%!PS-Adobe-3.0 EPSF-3.0\n'\
                        '%%BoundingBox: 0 0 ' + str(int(self.layout.width))\
                        + ' ' + str(int(self.layout.height))\
                        + '\n' + '%%HiResBoundingBox: 0 0 '\
                        + round_str(self.layout.width) + ' '\
                        + round_str(self.layout.height)\
                        + '\n\n' + round_str(self.line_width) + ' setlinewidth\n\n'\
                        + '/' + self.font + ' findfont '\
                        + round_str(self.font_normal_size)\
                        +  ' scalefont setfont\n' \
                        '/centershow\n'\
                        '{dup stringwidth pop\n'\
                        '2 div neg\n'\
                        '0 rmoveto\n'\
                        'show} def\n\n'\
                        '/rightshow\n'\
                        '{dup stringwidth pop\n'\
                        'neg\n'\
                        '0 rmoveto\n'\
                        'show} def\n\n'
        file_path = file_path if file_path else config.sub_folder\
            + config.file_name
        file = open(file_path, 'w')
        file.write(header+self.script)
        file.close()
        return self.script

    def summary(self):
        summary = {'line width':self.line_width,
                'font':self.font,
                'font normal size[pt]':self.font_normal_size,
                'layout rack_interval[pt]':self.layout.rack_interval,
                'layout scaling[mono/pt]':self.layout.scaling,
                'layout size[pt x pt]':round_str(self.layout.width) + 'x'
                + round_str(self.layout.height)}
        summary.update(self.layout.summary())
        return summary


def round_str(num):
    return str(round(float(num), int(config.number_of_decimal_places)))


def comment(txt, indent):
    return ' ' * indent + '%' + txt + '\n'


def newpath(indent, colour='0 0 0', line_width=config.line_width):
    return \
    ' ' * indent + 'newpath\n' +\
    ' ' * indent + colour + ' setrgbcolor\n' +\
    ' ' * indent + round_str(line_width) + ' setlinewidth\n'


def closepath(indent, colour='1 1 1'):
    return  \
    ' ' * indent + 'closepath\n' + \
    ' ' * indent + 'gsave\n' + \
    ' ' * indent + colour + ' setrgbcolor\n' + \
    ' ' * indent + 'fill\n' + \
    ' ' * indent + 'grestore\n' + \
    ' ' * indent + '0 0 0 setrgbcolor\n'


def stroke(indent):
    return \
    ' ' * indent + 'stroke\n' +\
    ' ' * indent + '0 0 0 setrgbcolor\n' +\
    ' ' * indent + round_str(config.line_width) + ' setlinewidth\n'\


def lt(x, y, indent):
    return ' ' * indent + round_str(x) + ' ' + round_str(y) + ' lineto\n'


def mt(x, y, indent):
    return ' ' * indent + round_str(x) + ' ' + round_str(y) + ' moveto\n'


def center_txt(x, y, txt, font, font_size, indent):
    return \
    ' ' * indent + '/' + font + ' findfont ' + round_str(font_size)\
        + ' scalefont setfont\n' + \
    ' ' * indent + round_str(x) + ' ' + round_str(y-font_size/3)\
        + ' moveto\n' + \
    ' ' * indent + '(' + str(txt) + ') centershow\n'


def show_txt(x, y, txt, font, font_size, indent):
    return \
    ' ' * indent + '/' + font + ' findfont ' + round_str(font_size)\
        + ' scalefont setfont\n' + \
    ' ' * indent + round_str(x) + ' ' + round_str(y) + ' moveto\n' + \
    ' ' * indent + '(' + str(txt) + ') show\n'


def right_txt(x, y, txt, font, font_size, indent):
    return \
    ' ' * indent + '/' + font + ' findfont ' + round_str(font_size)\
        + ' scalefont setfont\n' + \
    ' ' * indent + round_str(x) + ' ' + round_str(y-font_size/3)\
        + ' moveto\n' + \
    ' ' * indent + '(' + str(txt) + ') rightshow\n'
