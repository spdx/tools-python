#  Copyright (c) 2023 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from conversion.message import print_missing_conversion
from spdx3.model.software.snippet import Snippet

from spdx3.model.creation_information import CreationInformation

from spdx.model.snippet import Snippet as Snippet2


def convert_snippet(snippet2: Snippet2, creation_information: CreationInformation) -> Snippet:
    spdx_id = snippet2.spdx_id
    print("\n")
    print_missing_conversion("snippet.file_spdx_id", 0)
    byte_range = snippet2.byte_range
    line_range = snippet2.line_range
    print_missing_conversion("snippet.concluded_license, snippet.license_info_in_snippet, snippet.license_comment,"
                             "snippet.copyright_text", 0, "missing definitions for license profile")
    comment = snippet2.comment
    name = snippet2.name

    print_missing_conversion("snippet.attribution_texts", 0, "missing definitions for license profile")

    snippet = Snippet(spdx_id=spdx_id, creation_info=creation_information, byte_range=byte_range, line_range=line_range,
                      comment=comment, name=name)

    return snippet
