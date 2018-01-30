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
from collections import namedtuple

from extlib.bottle import bottle

from cyglib import form
from cyglib.config import config

from cyglib import cyginput


class BasicWebUI():
    def __init__(self, post_names):
        def format_post_string(key):
            obj = bottle.request.POST.getunicode(key)
            if isinstance(obj, str):
                obj = re.sub('\n+', '\n', obj.replace(' ', '').replace('\t', '').strip())
            return obj

        self.post_names = post_names
        self.post_dct = {i:format_post_string(i) for i in self.post_names}
        Post = namedtuple('Post', self.post_names)
        self.post = Post(**self.post_dct)

    def summary(self):
        summary = self.post_dct
        summary['matching_probe'] = summary['matching_probe'][0:30]

        summary.update(self.usr_input.summary())

        return summary

    def process_post(self):
        try:
            #title
            self.title = config.title
            self.show_title = self.post.show_title  == 'checked'
            self.title_position = self.post.title_position

            #scale bar
            self.show_scale_bar = self.post.show_scale_bar == 'checked'
            self.scale_bar_position = self.post.scale_bar_position
            self.scale_bar_unit = self.post.scale_bar_unit
            if self.show_scale_bar:
                try:
                    self.len_scale_bar = int(self.post.len_scale_bar)
                except ValueError:
                    print('ValueError Occurred. A value in "Scale Bar Length" were incorrect. The scale-bar option was ignored.')
                    self.show_scale_bar = None

            #Shaft
            self.show_shaft = True

            return True

        except KeyError:
            return 'KeyError'

    def process_request(self):
        if self.show_title:
            self.usr_input.accepts_request('Title',self.usr_input.top, name=self.title, option=self.title_position)
        if self.show_scale_bar:
            self.usr_input.accepts_request('ScaleBar', self.usr_input.bottom, end=self.len_scale_bar, name=self.scale_bar_unit, option=self.scale_bar_position)

    def download(self):
        #autorescale
        self.auto_rescale = self.post.auto_rescale  == 'checked'
        self.output_width_without_margin = len(self.seq)
        if self.auto_rescale:
            try:
                self.output_width_without_margin = int(self.post.output_width)
            except ValueError:
                print('ValueError Occurred. A value in "output_width" were incorrect. The auto-scaling was carried out default setting.')
        if self.auto_rescale:
           self.usr_input.rescale(self.output_width_without_margin)

        eps_file_path = config.sub_folder + config.file_name_head + self.title + config.extend
        self.usr_input.makes_eps_file(file_path=eps_file_path)

        del self.usr_input

        return [bottle.static_file(eps_file_path, root='.', download=eps_file_path),
               bottle.static_file("file.csv", root='.', download="file.csv") ]


class DirectSeqInputUI(BasicWebUI):
    def process_post(self):
        super().process_post()

        #title
        self.title = self.post.title

        #sites
        self.site_post = self.post.site
        self.site_column = form.new_column_index(name=0, pattern=1, position_on_pattern=2)

        #sequence
        self.seq = self.post.seq

        #boxes
        self.box_post = self.post.box
        self.box_column = form.new_column_index(name=0, start=1, end=2)

        #arrows
        self.arrow_post = self.post.arrow
        self.arrow_column = form.new_column_index(name=0, start=1, end=2)

        #probes
        self.probe_post = self.post.probe
        self.probe_column = form.new_column_index(name=0, start=1, end=2)

        #Shaft
        self.show_shaft = None if not self.post.show_shaft == 'checked' else True

        #Clipping
        self.clip_start = 1
        self.clip_end = len(self.seq)
        try:
            self.clipping = self.post.clipping == 'checked'
            if self.clipping:
                self.clip_start = int(self.post.clip_start)
                self.clip_end = int(self.post.clip_end)
        except:
            self.clipping = None
            print('ValueError Occurred. Values in "clip_start/end" were incorrect. Clipping option was ignored.')
        self.usr_input = cyginput.new_input(seq=self.seq)

    def process_request(self):

        super().process_request()

        [self.usr_input.accepts_request_from_post('Site', i, 'auto', column_index = self.site_column, with_shaft=self.show_shaft) for i in self.site_post.split(config.large_sep)]
        self.usr_input.accepts_request_from_post('Box', self.box_post, 'auto', column_index = self.box_column, with_shaft=self.show_shaft)
        self.usr_input.accepts_request_from_post('Arrow', self.arrow_post, 'auto', column_index = self.arrow_column, with_shaft=self.show_shaft)
        self.usr_input.accepts_request_from_post('Probe', self.probe_post, 'auto', column_index = self.probe_column, with_shaft=None)

        if self.clipping:
            self.usr_input.clip(clip_start=self.clip_start, clip_end=self.clip_end)


class IDInputUI(BasicWebUI):
    def process_post(self):
        super().process_post()

        ens_id = self.post.id
        get_exp = self.post.get_expand == 'checked'

        exp5 = 0
        exp3 = 0
        if get_exp:
            try:
                exp5 = int(self.post.expand5prime)
                exp3 = int(self.post.expand3prime)
            except ValueError:
                print('ValueError:ivalid input were detected in flanking sequence.')
        self.usr_input = cyginput.import_ensembl(ens_id, exp5, exp3, exon_num=self.post.exon_num_outer)

        if self.usr_input == 'KeyError':
            return 'KeyError'

        #title
        self.title = self.usr_input.genomeloc.display_name

        #sequence
        self.seq = self.usr_input.seq

        #sites
        self.site_post = self.post.site
        self.site_column = form.new_column_index(name=0, pattern=1, position_on_pattern=2)

        #SNP
        self.snp_query = re.split(config.small_sep+'|'+config.large_sep, self.post.snp)

        #InfMet
        if self.post.show_all_infmet == 'checked':
            self.query = 'all'
        else:
            self.query = re.split(config.small_sep+'|'+config.large_sep, self.post.infmet)

        #probes
        self.matching_probe_post = self.post.matching_probe
        self.matching_probe_column = form.new_column_index(name=0, pattern=1)

    def process_request(self):
        super().process_request()

        [self.usr_input.accepts_request_from_post('Site', i, 'auto', column_index = self.site_column, with_shaft=self.show_shaft) for i in self.site_post.split(config.large_sep)]
        if self.snp_query[-1]:
            self.usr_input.pull_rack()
            self.usr_input.accepts_request('SNP', 1, name=self.snp_query, with_shaft=None)
        self.usr_input.accepts_request('InfMet',self.usr_input.upper, name=self.query, option=self.post.infmet_platform, with_shaft=None)
        self.usr_input.recalls_reservation('all')
        self.usr_input.accepts_request_from_post('MatchingProbe', self.matching_probe_post, 'auto', column_index = self.matching_probe_column, with_shaft=None)
