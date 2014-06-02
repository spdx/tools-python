# Copyright 2014 Ahmed H. Ismail

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import csv
import os


class TwoWayDict(dict):
    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)
    def __delitem__(self, key):
        dict.__delitem__(self, self[key])
        dict.__delitem__(self, key)
            

def load_license_list():
    FILE_NAME = os.path.join(os.path.dirname(__file__), 'spdx_licenselist_v1.19.csv')
    with open(FILE_NAME, 'rb') as file:
        reader = csv.DictReader(file)
        dict = TwoWayDict()
        for entry in reader:
            dict[entry['Full name of License']] = entry['License Identifier']
    return dict



LICENSE_MAP = load_license_list()
LICENSE_LIST_VERSION = '1.19'



