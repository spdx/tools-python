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

from src.model.typing.dataclass_with_properties import dataclass_with_properties
from src.model.typing.type_checks import check_types_and_set_values


@dataclass_with_properties
class LicenseExpression:
    """So far, this just holds a string with the license expression. The ticket for adding license expression support
    is https://github.com/spdx/tools-python/issues/10."""
    expression_string: str

    def __init__(self, expression_string: str):
        check_types_and_set_values(self, locals())
