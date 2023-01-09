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

from typing import List

from spdx.model.package import ExternalPackageRef
from spdx.validation.validation_message import ValidationMessage


def validate_external_package_refs(external_package_refs: List[ExternalPackageRef], parent_id: str) -> List[
    ValidationMessage]:
    validation_messages = []
    for external_package_ref in external_package_refs:
        validation_messages.extend(validate_external_package_ref(external_package_ref, parent_id))

    return validation_messages


def validate_external_package_ref(external_package_ref: ExternalPackageRef, parent_id: str) -> List[ValidationMessage]:
    # TODO: https://github.com/spdx/tools-python/issues/373
    return []
