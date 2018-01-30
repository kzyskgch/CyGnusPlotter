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
import urllib
import urllib.request
import json
import time
from cyglib import form
from cyglib.config import config


class DBclient():

    def get_from_rest(self, url):
        start = time.time()
        request_handle = urllib.request.Request(url)
        request_result = urllib.request.urlopen(request_handle)
        text = request_result.read().decode('utf-8')
        print('fetching time from ' + url + ': \n\t' + str(time.time()-start) + '[sec]')
        return text

    def search_transcript(self, exp5=0):
        self.leader_exon = 1
        try:
            url_lookup = "http://rest.ensembl.org/lookup/id/" +\
                        self.identifier +\
                        "?content-type=application/json;expand=1"
            lookup_result = self.get_from_rest(url_lookup)
            rjson = json.loads(lookup_result)

            if rjson['object_type'] == 'Gene':
                for transcript in rjson['Transcript'][:]:
                    if transcript['is_canonical']:
                        self.identifier = transcript['id']
                        rjson = transcript
                        for exon in transcript['Exon']:
                            if ( exon['end'] + exp5 ) < transcript['start']:
                                self.leader_exon = self.leader_exon + 1
            return rjson

        except urllib.error.HTTPError:
            try:
                idlst = self.identifier.split(config.small_sep)

                symbol = idlst[0]
                species = idlst[1] if len(idlst) >= 2 else 'homo_sapiens'

                symbol_result = self.get_from_rest(
                                                    'http://rest.ensembl.org'
                                                    '/xrefs'
                                                    '/symbol/'
                                                   + species
                                                   + '/'+ symbol
                                                   + '?content-type=application'
                                                   '/json'
                                                   )
                self.identifier = json.loads(symbol_result)[0]['id']
                return self.search_transcript(exp5)

            except (urllib.error.HTTPError, IndexError):
                self.identifier = ''
                self.exp5 = 0
                self.exp3 = 0
                return {
                        'display_name':
                            'your_input_was_neither_an_ID_nor_a_genesymbol',
                        'start':0,
                        'end':0,
                        'strand':1,
                        'assembly_name':'',
                        'seq_region_name':''
                        }


class EnsemblClientForSeq(DBclient):

    def __init__(self, identifier, exp5, exp3):
        self.identifier = identifier
        self.exp5 = exp5
        self.exp3 = exp3

        rjson = self.search_transcript(exp5)

        display_name =  rjson['display_name']  if 'display_name' in rjson.keys()\
                        else str(self.identifier)

        strand = rjson['strand']

        if strand>0:
            start = rjson['start'] - exp5
            end = rjson['end'] + exp3
        else:
            start = rjson['start'] - exp3
            end = rjson['end'] + exp5

        url_seq = self.make_seq_url()
        req_seq = self.get_from_rest(url_seq) if self.identifier else 'N' * 500

        seq = req_seq[0:max(self.exp5, 0)].lower()\
            + req_seq[max(self.exp5, 0):(len(req_seq)-self.exp3)]\
            + req_seq[(len(req_seq)-self.exp3):].lower()

        self.result = form.new_genomeloc(seq=seq,
                                display_name=display_name,
                                assembly_name=rjson['assembly_name'],
                                seq_region_name=rjson['seq_region_name'],
                                start=start,
                                end=end,
                                strand=strand
                                )

    def make_seq_url(self):
        return 'http://rest.ensembl.org/sequence/id/' + self.identifier +\
        '?content-type=text/plain;' +\
        'expand_5prime=' + str(self.exp5) + ';' +\
        'expand_3prime=' + str(self.exp3) + ';' +\
        'mask_feature=1'


class EnsemblClientForSNP(DBclient):

    def __init__(self, probe_id_group, genomeloc):
        self.found_name = list()
        self.found_position = list()

        for i in probe_id_group:

            url = 'http://rest.ensembl.org/variation/human/' + i + \
            '?content-type=application/json'

            request_return = self.get_from_rest(url)
            as_dict = json.loads(request_return)
            try:
                mappings = as_dict['mappings'][0]

                added_position = None

                for j in mappings:
                    if genomeloc.end>=mappings['start']\
                    and genomeloc.start<=mappings['start']\
                    and genomeloc.assembly_name == mappings['assembly_name']\
                    and genomeloc.seq_region_name == mappings['seq_region_name']:

                        added_position = mappings['start'] - genomeloc.start\
                        if genomeloc.strand >0 \
                        else genomeloc.end - mappings['start'] -1

                if added_position:
                    self.found_name.append(i)
                    self.found_position.append(added_position)
            except KeyError:
                print('KeyError on SNP')