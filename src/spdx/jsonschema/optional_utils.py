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
from typing import Callable, TypeVar, Optional

T = TypeVar("T")
S = TypeVar("S")


def apply_if_present(function: Callable[[T], S], optional_value: Optional[T]) -> Optional[S]:
    """
    Apply the passed function to the optional value if it is not None. Else returns None.
    """
    return function(optional_value) if optional_value is not None else None
