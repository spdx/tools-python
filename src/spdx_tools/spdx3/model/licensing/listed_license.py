# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values

from .license import License


@dataclass_with_properties
class ListedLicense(License):
    list_version_added: Optional[str] = None
    deprecated_version: Optional[str] = None

    def __init__(
        self,
        license_id: str,
        license_name: str,
        license_text: str,
        license_comment: Optional[str] = None,
        see_also: List[str] = [],
        is_osi_approved: Optional[bool] = None,
        is_fsf_libre: Optional[bool] = None,
        standard_license_header: Optional[str] = None,
        standard_license_template: Optional[str] = None,
        is_deprecated_license_id: Optional[bool] = None,
        obsoleted_by: Optional[str] = None,
        list_version_added: Optional[str] = None,
        deprecated_version: Optional[str] = None,
    ):
        see_also = [] if not see_also else see_also
        check_types_and_set_values(self, locals())
