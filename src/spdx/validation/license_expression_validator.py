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

from typing import List, Optional, Union

from license_expression import LicenseExpression
from spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx.model.spdx_none import SpdxNone
from spdx.validation.validation_message import ValidationMessage


def validate_license_expressions(license_expressions: Optional[
    Union[List[LicenseExpression], SpdxNoAssertion, SpdxNone]]) -> List[ValidationMessage]:
    if license_expressions in [SpdxNoAssertion(), SpdxNone(), None]:
        return []

    error_messages = []

    for license_expression in license_expressions:
        error_messages.extend(validate_license_expression(license_expression))

    return error_messages


def validate_license_expression(license_expression: LicenseExpression) -> List[ValidationMessage]:
    # TODO: implement this once we have a better license expression model: https://github.com/spdx/tools-python/issues/374
    return []
