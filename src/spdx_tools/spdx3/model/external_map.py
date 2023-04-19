# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from dataclasses import field
from typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model.integrity_method import IntegrityMethod


@dataclass_with_properties
class ExternalMap:
    external_id: str  # anyURI
    verified_using: Optional[List[IntegrityMethod]] = field(default_factory=list)
    location_hint: Optional[str] = None  # anyURI

    def __init__(
        self,
        external_id: str,
        verified_using: Optional[List[IntegrityMethod]] = None,
        location_hint: Optional[str] = None,
    ):
        verified_using = [] if verified_using is None else verified_using
        check_types_and_set_values(self, locals())
