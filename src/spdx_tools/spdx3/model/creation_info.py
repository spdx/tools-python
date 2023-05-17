# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime
from typing import List, Optional

from semantic_version import Version

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model import ProfileIdentifier


@dataclass_with_properties
class CreationInfo:
    spec_version: Version
    created: datetime
    created_by: List[str]  # SPDXID of Agents
    created_using: List[str]  # SPDXID of Tools
    profile: List[ProfileIdentifier]
    data_license: str
    comment: Optional[str] = None

    def __init__(
        self,
        spec_version: Version,
        created: datetime,
        created_by: List[str],
        created_using: List[str],
        profile: List[ProfileIdentifier],
        data_license: str = "CC0",
        comment: Optional[str] = None,
    ):
        check_types_and_set_values(self, locals())
