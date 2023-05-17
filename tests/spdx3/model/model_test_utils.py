# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import Any, List, Type


def get_property_names(clazz: Type[Any]) -> List[str]:
    return [
        attribute
        for attribute in dir(clazz)
        if not attribute.startswith("_") and not callable(getattr(clazz, attribute))
    ]


class InvalidTypeClass:
    pass
