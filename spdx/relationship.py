# Copyright (c) 2020 Shubham Kumar Jha
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
from __future__ import unicode_literals

from functools import total_ordering


@total_ordering
class Relationshp(object):
    """
    Document relationship information
    Fields:
    - relationship: 
    """
    def __init__(self, relationship=None, relationship_comment=None):
        self.relationship = relationship
        self.relationship_comment = relationship_comment
    

    def __eq__(self, other):
        return (
            isinstance(other, Relationshp) and
            self.relationship == other.relationship and
            self.relationship_comment == other.relationship_comment
        )
    

    def __lt__(self, other):
        return (
            (self.relationship, self.relationship_comment) <
            (other.relationship, other.relationship_comment)
        )
    
    def validate(self, messages):
        """Returns True if all the fields are valid.
        Appends any error messages to messages parameter.
        """
        messages = self.validate_relationship(messages)

        return messages

    def validate_relationship(self, messages):
        if self.relationship is None:
            messages = messages + ['Relationship missing relationship']
        
        return messages