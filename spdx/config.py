
# Copyright (c) 2014 Ahmed H. Ismail
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import print_function

import csv
import os

from spdx.version import Version


class TwoWayDict(dict):

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)

    def __delitem__(self, key):
        dict.__delitem__(self, self[key])
        dict.__delitem__(self, key)


def load_license_list():
    FILE_NAME = os.path.join(os.path.dirname(__file__), 'spdx_licenselist.csv')
    with open(FILE_NAME, 'rb') as file_in:
        reader = csv.DictReader(file_in)
        dct = TwoWayDict()
        for entry in reader:
            dct[entry['Full name of License']] = entry['License Identifier']
    return dct


LICENSE_MAP = load_license_list()
LICENSE_LIST_VERSION = Version(major=1, minor=19)
