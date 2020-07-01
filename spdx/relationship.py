# Copyright (c) 2020 Yash Varshney

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
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
class Relationship(object):
    """
    Document relationship information
    Fields:
    - relationship:  provides information about the relationship between two SPDX elements.
    - relationship_comment :  place for the SPDX file creator to record any general comments. Optional, One
    """

    def __init__(self, relationship=None, relationship_comment=None):
        self.relationship = relationship
        self.relationship_comment = relationship_comment

    def __eq__(self, other):
        return (
            isinstance(other, Relationship)
            and self.relationship == other.relationship
            and self.relationship_comment == other.relationship_comment
        )

    def __lt__(self, other):
        return (self.relationship, self.relationship_comment) < (
            other.relationship,
            other.relationship_comment,
        )

    @property
    def has_comment(self):
        return self.relationship_comment is not None

    def validate(self, messages):
        """Returns True if all the fields are valid.
        Appends any error messages to messages parameter.
        """
        messages = self.validate_relationship(messages)

        return messages

    def validate_relationship(self, messages):
        messages = messages if messages is not None else []
        r_type = self.relationship.split(" ")[1]
        if r_type not in [
            None,
            "AMENDS",
            "OTHER",
            "COPY_OF",
            "TEST_OF",
            "ANCESTOR_OF",
            "BUILD_DEPENDENCY_OF",
            "BUILD_TOOL_OF",
            "CONTAINED_BY",
            "CONTAINS",
            "DATA_FILE_OF",
            "DEPENDENCY_MANIFEST_OF",
            "DEPENDENCY_OF",
            "DEPENDS_ON",
            "DESCENDANT_OF",
            "DESCRIBED_BY",
            "DESCRIBES",
            "DEV_DEPENDENCY_OF",
            "DEV_TOOL_OF",
            "DISTRIBUTION_ARTIFACT",
            "DOCUMENTATION_OF",
            "DYNAMIC_LINK",
            "EXAMPLE_OF",
            "EXPANDED_FROM_ARCHIVE",
            "FILE_ADDED",
            "FILE_DELETED",
            "FILE_MODIFIED",
            "GENERATED_FROM",
            "GENERATES",
            "HAS_PREREQUISITE",
            "METAFILE_OF",
            "OPTIONAL_COMPONENT_OF",
            "OPTIONAL_DEPENDENCY_OF",
            "PACKAGE_OF",
            "PATCH_APPLIED",
            "PATCH_FOR",
            "PREREQUISITE_FOR",
            "PROVIDED_DEPENDENCY_OF",
            "RUNTIME_DEPENDENCY_OF",
            "STATIC_LINK",
            "TEST_CASE_OF",
            "TEST_DEPENDENCY_OF",
            "TEST_TOOL_OF",
            "VARIANT_OF",
        ]:

            messages = messages + [
                "Relationship type must be one of the constants defined in "
                "class spdx.relationship.Relationship"
            ]
            return messages
        else:
            return True
