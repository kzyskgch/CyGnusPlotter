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
import os, glob

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir('../')

parent = os.getcwd() + '/'

target = [
        parent+'cyglib/__pycache__',
        parent+'cyglib/components/__pycache__',
        parent+'extlib/__pycache__',
        parent+'extlib/bottle/__pycache__',
        ]

for path in target:
    print(path)
    os.chdir(path)
    for pyc in glob.glob('*.pyc'):
        os.remove(pyc)

