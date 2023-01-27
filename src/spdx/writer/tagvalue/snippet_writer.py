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
from typing import TextIO

from spdx.model.snippet import Snippet
from spdx.writer.tagvalue.tagvalue_writer_helper_functions import write_value, write_text_value, write_range, \
    write_license_info_list


def write_snippet(snippet: Snippet, output_text: TextIO):
    output_text.write("## Snippet Information\n")

    write_value("SnippetSPDXID", snippet.spdx_id, output_text)
    write_value("SnippetFromFileSPDXID", snippet.file_spdx_id, output_text)
    write_range("SnippetByteRange", snippet.byte_range, output_text)
    write_range("SnippetLineRange", snippet.line_range, output_text)

    write_value("SnippetLicenseConcluded", snippet.license_concluded, output_text)
    write_license_info_list("LicenseInfoInSnippet", snippet.license_info_in_snippet, output_text)
    write_text_value("SnippetLicenseComments", snippet.license_comment, output_text)
    write_text_value("SnippetCopyrightText", snippet.copyright_text, output_text)

    write_text_value("SnippetComment", snippet.comment, output_text)
    write_value("SnippetName", snippet.name, output_text)

    for attribution_text in snippet.attribution_texts:
        write_text_value("SnippetAttributionText", attribution_text, output_text)
