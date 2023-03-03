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

from spdx.model.file import File
from spdx.writer.tagvalue.checksum_writer import write_checksum_to_tag_value
from spdx.writer.tagvalue.tagvalue_writer_helper_functions import write_value, write_text_value


def write_file(file: File, text_output: TextIO):
    text_output.write("## File Information\n")

    write_value("FileName", file.name, text_output)
    write_value("SPDXID", file.spdx_id, text_output)

    for file_type in file.file_types:
        write_value("FileType", file_type.name, text_output)

    for file_checksum in file.checksums:
        write_value("FileChecksum", write_checksum_to_tag_value(file_checksum), text_output)

    write_value("LicenseConcluded", file.license_concluded, text_output)
    for license_info in file.license_info_in_file:
        write_value("LicenseInfoInFile", license_info, text_output)
    write_text_value("LicenseComments", file.license_comment, text_output)
    write_text_value("FileCopyrightText", file.copyright_text, text_output)

    write_text_value("FileComment", file.comment, text_output)
    write_text_value("FileNotice", file.notice, text_output)

    for contributor in sorted(file.contributors):
        write_value("FileContributor", contributor, text_output)

    for attribution_text in file.attribution_texts:
        write_text_value("FileAttributionText", attribution_text, text_output)
