#!/usr/bin/env python3
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
import os, glob, webbrowser
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from cyglib.config import config
from cyglib import cyghost


if __name__ == '__main__':
    cyghost.system_check()

    if not config.sub_folder.replace('./','').replace('/','') in os.listdir():
        os.mkdir(config.sub_folder)
    def run_server(host, port, open_browser=True):
        if open_browser:
            browser = webbrowser.get()
            browser.open_new('http://' + host + ':' + str(port) + '/')
        cyghost.bottle.run(host=host, port=port)
        [os.remove(f) for f in glob.glob("./temp/*.eps")]

    host = str(config.host)
    port = str(round(config.port))

    run_server(host, port)
