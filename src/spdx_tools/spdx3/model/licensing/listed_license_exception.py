# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model.licensing.license_addition import LicenseAddition


@dataclass_with_properties
class ListedLicenseException(LicenseAddition):
    list_version_added: Optional[str] = None
    deprecated_version: Optional[str] = None

    def __init__(
        self,
        addition_id: str,
        addition_name: str,
        addition_text: str,
        addition_comment: Optional[str] = None,
        see_also: List[str] = None,
        standard_addition_template: Optional[str] = None,
        is_deprecated_addition_id: Optional[bool] = None,
        obsoleted_by: Optional[str] = None,
        list_version_added: Optional[str] = None,
        deprecated_version: Optional[str] = None,
    ):
        see_also = [] if see_also is None else see_also
        check_types_and_set_values(self, locals())
