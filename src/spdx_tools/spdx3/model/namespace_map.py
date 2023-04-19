# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values


@dataclass_with_properties
class NamespaceMap:
    prefix: Optional[str] = None
    namespace: Optional[str] = None  # anyURI

    def __init__(self, prefix: Optional[str] = None, namespace: Optional[str] = None):
        check_types_and_set_values(self, locals())
