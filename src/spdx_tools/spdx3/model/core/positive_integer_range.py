# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values


@dataclass_with_properties
class PositiveIntegerRange:
    begin: int
    end: int

    def __init__(
        self,
        begin: int,
        end: int,
    ):
        check_types_and_set_values(self, locals())
