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
class Version(object):
    """Version number composed of major and minor.
       Fields:
       major: Major number, int.
       minor: Minor number, int.
    """
    def __init__(self, major=1, minor=2):
        super(Version, self).__init__()
        self.major = major
        self.minor = minor
        
    def __cmp__(self, other):
        if self.major == other.major:
            return self.minor - other.minor
        elif self.major < other.major:
            return -1
        else:
            return 1