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
import os
from extlib.bottle import bottle
from cyglib import guimethod


@bottle.route('/')
def home():
    return bottle.static_file('index.html', root= os.getcwd() + './html')


@bottle.route('/cygnus/<file_path>')
def html(file_path):
    return bottle.static_file(file_path, root= './html'),


@bottle.route('/<file_path>')
def image(file_path):
    return bottle.static_file(file_path, root= './image')


@bottle.route('/by_sequence/', method=['POST'])
def by_sequence():
    post_names = ['title', 'show_title', 'title_position',
                  'seq', 'site',  'box', 'arrow' , 'probe',
                  'clipping', 'clip_start', 'clip_end',
                  'show_scale_bar', 'len_scale_bar', 'scale_bar_unit', 'scale_bar_position',
                  'show_shaft', 'auto_rescale', 'output_width']
    usr_method = guimethod.DirectSeqInputUI(post_names)
    check = usr_method.process_post()
    if check == "KeyError":
        return bottle.static_file('keyerror.html', root = '/html')
    usr_method.process_request()
    return usr_method.download()


@bottle.route('/by_ensembl_id/', method=['POST'])
def by_ensembl_id():
    post_names = ['id', 'get_expand', 'expand5prime', 'expand3prime', 'exon_num_outer',
                  'show_title', 'title_position',
                  'site', 'infmet', 'show_all_infmet', 'infmet_platform', 'probe',
                  'snp', 'matching_probe','show_scale_bar', 'len_scale_bar',
                  'scale_bar_unit', 'scale_bar_position',
                  'auto_rescale', 'output_width']
    usr_method = guimethod.IDInputUI(post_names)
    check = usr_method.process_post()
    if check == "KeyError":
        return bottle.static_file('keyerror.html', root= os.getcwd() + '/html')

    usr_method.process_request()
    return usr_method.download()

def system_check():
    pass