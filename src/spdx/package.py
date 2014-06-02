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
class Package(object):
    """Represents an analyzed Package.
    Fields:
        name : Mandatory, string.
        version: Optional, string.
        file_name: Optional, string.
        supplier: Optional, Organization or Person
        originator: Optional, Organization or Person.
        download_location: Mandatory, URL as string.
    """
    def __init__(self, name, download_location,version="", file_name="", 
            supplier=None, originator=None):
        super(Package, self).__init__()
        self.name = name
        self.version = version
        self.file_name = file_name
        self.supplier = supplier
        self.originator = originator
        self.download_location = download_location