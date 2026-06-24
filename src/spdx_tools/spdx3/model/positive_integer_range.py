# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values


@dataclass_with_properties
class PositiveIntegerRange:
    begin_integer_range: int
    end_integer_range: int

    def __init__(
        self,
        begin_integer_range: int,
        end_integer_range: int,
    ):
        check_types_and_set_values(self, locals())
