# Copyright (c) 2022 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
from typing import List, Optional

from spdx.model.extracted_licensing_info import ExtractedLicensingInfo
from spdx.validation.uri_validators import validate_url
from spdx.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


def validate_extracted_licensing_infos(extracted_licensing_infos: Optional[List[ExtractedLicensingInfo]]) -> List[
    ValidationMessage]:
    validation_messages = []
    for extracted_licensing_info in extracted_licensing_infos:
        validation_messages.extend(validate_extracted_licensing_info(extracted_licensing_info))

    return validation_messages


def validate_extracted_licensing_info(extracted_licensing_infos: ExtractedLicensingInfo) -> List[
    ValidationMessage]:
    validation_messages: List[ValidationMessage] = []
    context = ValidationContext(element_type=SpdxElementType.EXTRACTED_LICENSING_INFO,
                                full_element=extracted_licensing_infos)

    license_id: str = extracted_licensing_infos.license_id
    if license_id and not re.match(r"^LicenseRef-[\da-zA-Z.-]+$", license_id):
        validation_messages.append(
            ValidationMessage(
                f'license_id must only contain letters, numbers, "." and "-" and must begin with "LicenseRef-", but is: {license_id}',
                context)
        )

    if license_id and not extracted_licensing_infos.extracted_text:
        validation_messages.append(
            ValidationMessage("extracted_text must be provided if there is a license_id assigned", context)
        )

    for cross_reference in extracted_licensing_infos.cross_references:
        for message in validate_url(cross_reference):
            validation_messages.append(
                ValidationMessage("cross_reference " + message, context)
            )

    return validation_messages
