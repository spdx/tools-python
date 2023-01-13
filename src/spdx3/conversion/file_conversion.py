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
from spdx3.conversion.message import print_missing_conversion
from spdx3.model.software.file import File

from spdx3.model.creation_information import CreationInformation

from spdx.model.file import File as Spdx2_File


def convert_file(spdx2_file: Spdx2_File, creation_information: CreationInformation) -> File:
    name = spdx2_file.name
    spdx_id = spdx2_file.spdx_id
    # file.checksums -> file.verifiedUsing
    print("\n")
    print_missing_conversion("file.checksums", 1, "for IntegrityMethod")
    # file.file_types -> file.content_type (MediaType with Cardinality 1)
    print_missing_conversion("file.file_type", 0, "different cardinalities")
    print_missing_conversion(
        "file.concluded_license, file.license_info_in_file, file.license_comment, file.copyright_text", 0,
        "missing definition for license profile")

    comment = spdx2_file.comment
    print_missing_conversion("file.notice, file.contributors, file.attribution_texts", 0,
                             "missing definition for license profile")

    file = File(spdx_id, creation_info=creation_information, name=name, comment=comment)
    return file
