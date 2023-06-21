# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import List

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model.licensing.any_license_info import AnyLicenseInfo


@dataclass_with_properties
class DisjunctiveLicenseSet(AnyLicenseInfo):
    member: List[AnyLicenseInfo]

    def __init__(self, member: List[AnyLicenseInfo]):
        check_types_and_set_values(self, locals())
