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
import csv
from cyglib.config import config


main_data = list()
with open(config.data_folder+config.inf_met_filename, newline='') as f:
            reader = csv.reader(f, delimiter='\t')
            main_data = main_data + list(reader)

class Access():
    pass

class InfMetAccess(Access):

    def __init__(self, query, genomeloc, platform):

        self.temp_data = {row[2]:row[4] for row in main_data if
                     row[0]==genomeloc.assembly_name and
                     row[1]==platform and
                     row[3]==genomeloc.seq_region_name}

        self.data = dict()
        for k, v in self.temp_data.items():
            try:
                self.data[k] = int(v)
            except ValueError:
                pass#Incorrect value

        self.query = query
        self.start = genomeloc.start
        self.end = genomeloc.end
        self.strand = genomeloc.strand

        if query == 'all':
            self.result = self.position_all()

        else:
            self.result = self.position_by_id()

    def position_by_id(self):

        position = dict()

        for target_id in self.query:
            try:
                relative_location = int(self.data[target_id]) - self.start if self.strand>0 else self.end - int(self.data[target_id]) - 1
                if relative_location>0 and relative_location<=(self.end-self.start+1):
                    position[target_id] = relative_location
                    print('cg probe ' + target_id + ' was found.')
                else:
                    print('cg probe ' + target_id + ' was out of the sequence.')
            except KeyError:
                print(target_id + ' is not in data.')

        return position


    def position_all(self):

        if self.strand>0:
            data_in_region = {k: v - self.start for k, v in self.data.items() if v>=self.start and v<=self.end}
        else:
            data_in_region = {k: self.end - v - 1 for k, v in self.data.items() if (v+1)>=self.start and (v+1)<=self.end}

        [print('Infinium probe ' + str(k) + ' was founrd in ' + str(v) + '.') for k, v in data_in_region.items()]

        return data_in_region