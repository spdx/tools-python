# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import Callable, Optional, TypeVar

T = TypeVar("T")
S = TypeVar("S")


def apply_if_present(function: Callable[[T], S], optional_value: Optional[T]) -> Optional[S]:
    """
    Apply the passed function to the optional value if it is not None. Else returns None.
    """
    return function(optional_value) if optional_value is not None else None
