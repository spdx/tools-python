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
from typing import Tuple, Optional

from spdx import license
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
     - snip_from_file_spdxid:  Uniquely identify the file in an SPDX document
     which this snippet is associated with. Mandatory, one. Type: str.
     - conc_lics: Contains the license the SPDX file creator has concluded as
     governing the snippet or alternative values if the governing license
     cannot be determined. Mandatory one. Type: license.License or
     utils.NoAssert or utils.SPDXNone.
     - licenses_in_snippet: The list of licenses found in the snippet.
     Mandatory, one or more. Type: license.License or utils.SPDXNone or
     utils.NoAssert.
     - attribution_text: optional string.
     - byte_range: Defines the byte range in the original host file that the
     snippet information applies to. Mandatory, one. Type (int, int)
     - line_range: Defines the line range in the original host file that the
     snippet information applies to. Optional, one. Type (int, int)
    """

    def __init__(
        self, spdx_id=None, copyright=None, snip_from_file_spdxid=None, conc_lics=None, byte_range=None
    ):
        self.spdx_id = spdx_id
        self.name = None
        self.comment = None
        self.copyright = copyright
        self.license_comment = None
        self.attribution_text = None
        self.snip_from_file_spdxid = snip_from_file_spdxid
        self.conc_lics = conc_lics
        self.licenses_in_snippet = []
        self.byte_range: Optional[Tuple[int, int]] = byte_range
        self.line_range: Optional[Tuple[int, int]] = None

    def add_lics(self, lics):
        self.licenses_in_snippet.append(lics)

    def validate(self, messages):
        """
        Validate fields of the snippet and update the messages list with user
        friendly error messages for display.
        """
        self.validate_spdx_id(messages)
        self.validate_copyright_text(messages)
        self.validate_snip_from_file_spdxid(messages)
        self.validate_concluded_license(messages)
        self.validate_licenses_in_snippet(messages)

        return messages

    def validate_spdx_id(self, messages):
        if self.spdx_id is None:
            messages.append("Snippet has no SPDX Identifier.")

    def validate_copyright_text(self, messages):
        if self.copyright and not isinstance(
            self.copyright,
            (str, utils.NoAssert, utils.SPDXNone),
        ):
            messages.append(
                "Snippet copyright must be str or unicode or spdx.utils.NoAssert or spdx.utils.SPDXNone"
            )

    def validate_snip_from_file_spdxid(self, messages):
        if self.snip_from_file_spdxid is None:
            messages.append("Snippet has no Snippet from File SPDX Identifier.")

    def validate_concluded_license(self, messages):
        if self.conc_lics and not isinstance(
            self.conc_lics, (utils.SPDXNone, utils.NoAssert, license.License)
        ):
            messages.append(
                "Snippet concluded license must be instance of "
                "spdx.utils.SPDXNone or spdx.utils.NoAssert or "
                "spdx.license.License"
            )

    def validate_licenses_in_snippet(self, messages):
        for lic in self.licenses_in_snippet:
            if not isinstance(
                lic, (license.License, utils.NoAssert, utils.SPDXNone)
            ):
                messages.append(
                    "License in snippet must be instance of "
                    "spdx.utils.SPDXNone or spdx.utils.NoAssert or "
                    "spdx.license.License"
                )

    def has_optional_field(self, field):
        return bool(getattr(self, field, None))
