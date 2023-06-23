# SPDX-License-Identifier: Apache-2.0
#  Copyright (c) 2022 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from beartype.typing import TextIO

from spdx_tools.spdx.model import Snippet
from spdx_tools.spdx.writer.tagvalue.tagvalue_writer_helper_functions import write_range, write_text_value, write_value


def write_snippet(snippet: Snippet, text_output: TextIO):
    text_output.write("## Snippet Information\n")

    write_value("SnippetSPDXID", snippet.spdx_id, text_output)
    write_value("SnippetFromFileSPDXID", snippet.file_spdx_id, text_output)
    write_range("SnippetByteRange", snippet.byte_range, text_output)
    write_range("SnippetLineRange", snippet.line_range, text_output)

    write_value("SnippetLicenseConcluded", snippet.license_concluded, text_output)
    for license_info in snippet.license_info_in_snippet:
        write_value("LicenseInfoInSnippet", license_info, text_output)
    write_text_value("SnippetLicenseComments", snippet.license_comment, text_output)
    write_text_value("SnippetCopyrightText", snippet.copyright_text, text_output)

    write_text_value("SnippetComment", snippet.comment, text_output)
    write_value("SnippetName", snippet.name, text_output)

    for attribution_text in snippet.attribution_texts:
        write_text_value("SnippetAttributionText", attribution_text, text_output)
