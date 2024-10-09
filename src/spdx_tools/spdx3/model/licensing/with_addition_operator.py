# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model.licensing import AnyLicenseInfo, License, LicenseAddition


@dataclass_with_properties
class WithAdditionOperator(AnyLicenseInfo):
    subject_license: License
    subject_addition: LicenseAddition

    def __init__(self, subject_license: License, subject_addition: LicenseAddition):
        check_types_and_set_values(self, locals())
