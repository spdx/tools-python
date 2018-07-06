# Copyright (c) 2018 Yash M. Nisar
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import six

from spdx import utils


class Snippet(object):
    """
    Represents an analyzed snippet.
    Fields:
     - spdx_id: Uniquely identify any element in an SPDX document which may be
     referenced  by other elements. Mandatory, one per snippet if the snippet
     is present.
     - name: Name of the snippet. Optional, one. Type: str.
     - comment: General comments about the snippet. Optional, one. Type: str.
     - copyright: Copyright text. Mandatory, one. Type: str.
     - license_comment: Relevant background references or analysis that went
     in to arriving at the Concluded License for a snippet. Optional, one.
     Type: str.
    """

    def __init__(self, spdx_id=None, copyright=None):
        self.spdx_id = spdx_id
        self.name = None
        self.comment = None
        self.copyright = copyright
        self.license_comment = None

    def validate(self, messages=None):
        """
        Validate fields of the snippet and update the messages list with user
        friendly error messages for display.
        """
        # FIXME: we should return messages instead
        messages = messages if messages is not None else []

        return (self.validate_spdx_id(messages) and
                self.validate_copyright_text(messages))

    def validate_spdx_id(self, messages=None):
        # FIXME: messages should be returned
        messages = messages if messages is not None else []

        if self.spdx_id is None:
            messages.append('Snippet has no SPDX Identifier.')
            return False

        else:
            return True

    def validate_copyright_text(self, messages=None):
        # FIXME: we should return messages instead
        messages = messages if messages is not None else []

        if isinstance(
            self.copyright,
                (six.string_types, six.text_type, utils.NoAssert,
                 utils.SPDXNone)):
            return True
        else:
            messages.append('Snippet copyright must be str or unicode or '
                            'utils.NoAssert or utils.SPDXNone')
            return False

    def has_optional_field(self, field):
        return getattr(self, field, None) is not None