# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from dataclasses import field

from beartype.typing import List, Optional, Union

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx.model import SpdxNoAssertion


@dataclass_with_properties
class ExtractedLicensingInfo:
    license_id: Optional[str] = None
    extracted_text: Optional[str] = None
    license_name: Optional[Union[str, SpdxNoAssertion]] = None
    cross_references: List[str] = field(default_factory=list)
    comment: Optional[str] = None

    def __init__(
        self,
        license_id: Optional[str] = None,
        extracted_text: Optional[str] = None,
        license_name: Optional[Union[str, SpdxNoAssertion]] = None,
        cross_references: List[str] = None,
        comment: Optional[str] = None,
    ):
        cross_references = [] if cross_references is None else cross_references
        check_types_and_set_values(self, locals())
