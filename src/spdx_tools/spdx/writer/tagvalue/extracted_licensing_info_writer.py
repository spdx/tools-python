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

from spdx_tools.spdx.model import ExtractedLicensingInfo
from spdx_tools.spdx.writer.tagvalue.tagvalue_writer_helper_functions import write_text_value, write_value


def write_extracted_licensing_info(extracted_licensing_info: ExtractedLicensingInfo, text_output: TextIO):
    write_value("LicenseID", extracted_licensing_info.license_id, text_output)
    write_text_value("ExtractedText", extracted_licensing_info.extracted_text, text_output)
    write_value("LicenseName", extracted_licensing_info.license_name, text_output)

    for cross_reference in sorted(extracted_licensing_info.cross_references):
        write_value("LicenseCrossReference", cross_reference, text_output)

    write_text_value("LicenseComment", extracted_licensing_info.comment, text_output)
