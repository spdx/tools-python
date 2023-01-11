# Copyright (c) 2022 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from dataclasses import fields
from typing import Any, Dict

from spdx_tools.common.typing.constructor_type_errors import ConstructorTypeErrors


def check_types_and_set_values(instance_under_construction: Any, local_variables: Dict, origin_class: Any = None) -> None:
    """
    Helper method to accumulate all type errors encountered during a constructor call and return them in a
    ConstructorTypeErrors instance.
    Background: Our setters are enhanced with runtime typechecks using typeguard. However, this means that by
    default, a TypeError is raised on the first type violation that is encountered. We consider it more helpful to
    return all type violations in one go.
    As an aside, defining constructors "manually" using this utility method helps avoid a nasty PyCharm bug:
    https://youtrack.jetbrains.com/issue/PY-34569
    With the additional parameter origin_class we ensure that the attributes from the class that calls this method
    are set. If we use inheritance the instance_under_construction object might be a child object.
    """
    if not origin_class:
        origin_class = instance_under_construction
    errors = []
    for field in fields(instance_under_construction):
        key = field.name
        value = local_variables.get(key)
        try:
            setattr(instance_under_construction, key, value)
        except TypeError as err:
            error_message: str = err.args[0]
            errors.append(error_message)
    if errors:
        raise ConstructorTypeErrors(errors)
