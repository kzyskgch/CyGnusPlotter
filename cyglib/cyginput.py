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

from cyglib.config import config
from cyglib import form
from cyglib import component
from cyglib import dbclient

from cyglib import layout
from cyglib import eps


def new_input(seq = '', genomeloc=form.new_genomeloc() ,request_group = [], reserved_request_group=None):
    reserved_request_group = list() if not reserved_request_group else reserved_request_group
    return CyGInput(seq=seq, genomeloc=genomeloc, request_group=request_group, reserved_request_group=reserved_request_group)


def import_ensembl(ens_id, exp5, exp3, exons_to_boxes=True, exon_num='outer', with_shaft=True):
    #Fetching
    reply = dbclient.EnsemblClientForSeq(ens_id, exp5, exp3)
    seq = reply.result.seq

    #num of the repeat for exon num inner
    desplay_box_num = 1 if exon_num == 'inner' else 0

    import_input = new_input(seq=seq, genomeloc=reply.result)

    if exons_to_boxes:
        regex =  [find for find in re.finditer('[A-Z]+', seq)]
        box_lst = list()
        for i in range(len(regex)):
            find = regex[i]
            box_lst.append((str(reply.leader_exon+i) * desplay_box_num,
                            str(find.start()+1), str(find.end())))
        center_position = [(float(box[1])+float(box[2]))/2 for box in box_lst]

        box_post = config.large_sep.join([config.small_sep.join(box_lst[i])
            for i in range(0, len(box_lst))])
        box_column = form.new_column_index(name = 0, start = 1, end = 2)

        import_input.reserved_request_group.append(
                lambda:import_input.accepts_request_from_post('Box', box_post,
                'auto', column_index = box_column, with_shaft=with_shaft))

        #method for OuterBoxNum
        if exon_num == 'outer':
            lst_exon_num = [str(reply.leader_exon+i) for i in range(0,len(box_lst))]
            import_input.reserved_request_group.append(lambda:import_input.accepts_request('OuterBoxNum', 1, name=lst_exon_num, position_spot=center_position))
        else:
            import_input.reserved_request_group.append(lambda:None)

    return import_input


class CyGInput:
    def __init__(self, seq, genomeloc, request_group, reserved_request_group):

        self.seq = str(seq)
        self.genomeloc = genomeloc

        self.clip_start = 1
        self.clip_end = len(self.seq)
        self.request_group = list(request_group)
        self.reserved_request_group = reserved_request_group

        self.eps = eps.new_eps(layout.new_layout())

        self.rescale = self.eps.layout.rescale #The method self.rescale is deprecated.
        self.scales_layout = self.eps.layout.rescale
        self.top = self.eps.layout.top
        self.upper = self.eps.layout.upper
        self.bottom = self.eps.layout.bottom
        self.direct = self.eps.layout.direct
        self.writes_eps = self.eps.save

        self.clips_sequence = self.clip #This line is a transitional measure for the method self.clip is deprecated.

    def pull_rack(self):
        for i in range(0,len(self.request_group)):
            request = self.request_group[i]
            if isinstance(request.rack_order, (int, float)):
                self.request_group[i] = request._replace(rack_order = request.rack_order + 1)

    def auto_rack(self, rack_order):
        if rack_order=='auto':
            self.pull_rack()
            return 1
        else:
            return rack_order

    def accepts_request_insert(self, component_type, rack_order, insertion=0, with_shaft=None, **item):
        rack_order=self.auto_rack(rack_order)
        item_group = [form.new_item()._replace(**item)]
        self.request_group.insert(insertion, form.new_request(component_type=component_type,
                                                      rack_order=rack_order,
                                                      item_group=item_group))
        if with_shaft:
            self.request_group.insert(insertion, form.new_request(component_type='Shaft',
                                                                  rack_order=rack_order,
                                                  item_group=item_group))

    def accepts_request(self, component_type, rack_order, with_shaft=None, **item):

        self.accepts_request_insert(component_type, rack_order, len(self.request_group), with_shaft, **item)

    def accepts_request_from_post(self,
                                 component_type,
                                 post,
                                 rack_order,
                                 large_sep = config.large_sep,
                                 small_sep = config.small_sep,
                                 column_index = form.new_column_index(),
                                 with_shaft = None):

            if post == '':
                pass
            else:
                rack_order = self.auto_rack(rack_order)
                if with_shaft:
                    self.accepts_request('Shaft', rack_order)
                sep_post =  [i.split(small_sep) for i in post.split(large_sep)]
                item_group = list()
                for row in sep_post:
                    if isinstance(row, list):
                        new_item_as_list = list(form.new_item())
                        for i in range(0,len(new_item_as_list)):
                            index = column_index[i]
                            if isinstance(index, int):
                                new_item_as_list[i] = row[index]
                        new_item = form.new_item_from_list(new_item_as_list)
                        item_group.append(new_item)
                self.request_group.append(form.new_request(component_type=component_type,
                                                           rack_order=rack_order,
                                                           item_group=item_group))

    def clip(self, clip_start, clip_end):
        self.clip_start = clip_start if clip_start > 1 else 1
        self.clip_end = clip_end if clip_end > clip_start else clip_start

    def recalls_reservation(self, req_num='all'):
        if req_num == 'all':
            [i() for i in self.reserved_request_group]
            self.reserved_request_group = list()
        elif isinstance(req_num, int):
            self.reserved_request_group[req_num]()
            del self.reserved_request_group[req_num]

    def builds_components_on_requests(self, add=None):
        component_group = list()
        for request in self.request_group:
            try:
                for item in request.item_group:
                    component_group.append(eval('component.' + request.component_type)
                                              (request.rack_order, item, self.seq, self.genomeloc, self.clip_start, self.clip_end))
            except AttributeError:
                print('Wrong Component name might be inputted.')
        self.eps.gets_component_group(component_group, add)

    def makes_eps_file(self, file_path):
        self.builds_components_on_requests()
        self.writes_eps(file_path)

    def resets_requests(self, new_seq=None):
        if new_seq:
            self.seq = new_seq
        self.request_group = list()

    def shows_requests(self):
        print('#'.rjust(3)  + 'Component_type'.rjust(20) + 'name'.rjust(15) + 'rack_order'.rjust(12) + 'start'.rjust(12) + 'end'.rjust(12))
        for i in range(len(self.request_group)):
            req = self.request_group[i]
            if isinstance(req.item_group[0].name, str):
                print(str(i).rjust(3) + req.component_type.rjust(20) + req.item_group[0].name.rjust(15), end='')
            else:
                print(str(i).rjust(3) + req.component_type.rjust(20) + ''.rjust(15), end='')
            if isinstance(req.rack_order, (int, float)):
                print(str(req.rack_order).rjust(12), end='')
            else:
                print(req.rack_order.__name__.rjust(12), end='')
            print(str(req.item_group[0].start).rjust(12) + str(req.item_group[0].end).rjust(12))

    def accepts_cancel_request(self, cancel_num):
        del self.request_group[cancel_num]
        self.shows_requests()

    def summary(self):
        summary = {'seq length':len(self.seq),
                'head seq':self.seq[0:10],
                'tail seq':self.seq[-10:],
                'clip range':str(self.clip_start) + '-' + str(self.clip_end),
                '# of requests':str(len(self.request_group)), 'requests':[i.component_type for i in self.request_group]}
        summary.update(self.eps.summary())
        return summary
