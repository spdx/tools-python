# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from dataclasses import field
from datetime import datetime

from beartype.typing import List, Optional
from semantic_version import Version

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model import ProfileIdentifierType


@dataclass_with_properties
class CreationInfo:
    spec_version: Version
    created: datetime
    created_by: List[str]  # SPDXID of Agents
    profile: List[ProfileIdentifierType]
    data_license: Optional[str] = "CC0-1.0"
    created_using: List[str] = field(default_factory=list)  # SPDXID of Tools
    comment: Optional[str] = None

    def __init__(
        self,
        spec_version: Version,
        created: datetime,
        created_by: List[str],
        profile: List[ProfileIdentifierType],
        data_license: Optional[str] = "CC0-1.0",
        created_using: List[str] = None,
        comment: Optional[str] = None,
    ):
        created_using = [] if created_using is None else created_using
        check_types_and_set_values(self, locals())
