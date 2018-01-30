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

import os, sys, glob, re

CODEC = 'UTF8'
PATTERN = input('Input search word: ')

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir('../')

parent = os.getcwd() + '/'

target = [
        parent+'cyglib',
        parent+'cyglib/components',
        ]

for path in target:
    os.chdir(path)
    for py in glob.glob('*.py'):
        f = open(py, 'r', encoding=CODEC)
        script = f.readlines()

        cnt = 1

        for line in script:
            if re.search(PATTERN, line):
                print(py + ' ' + str(cnt) + ':\t' + line.replace(' ', '').replace('\n', '').rjust(30))
            cnt = cnt + 1
