# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from dataclasses import field

from beartype.typing import List, Optional, Tuple, Union
from license_expression import LicenseExpression

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx.model import SpdxNoAssertion, SpdxNone


@dataclass_with_properties
class Snippet:
    spdx_id: str
    file_spdx_id: str
    byte_range: Tuple[int, int]
    line_range: Optional[Tuple[int, int]] = None
    license_concluded: Optional[Union[LicenseExpression, SpdxNoAssertion, SpdxNone]] = None
    license_info_in_snippet: List[Union[LicenseExpression, SpdxNoAssertion, SpdxNone]] = None
    license_comment: Optional[str] = None
    copyright_text: Optional[Union[str, SpdxNoAssertion, SpdxNone]] = None
    comment: Optional[str] = None
    name: Optional[str] = None
    attribution_texts: List[str] = field(default_factory=list)

    def __init__(
        self,
        spdx_id: str,
        file_spdx_id: str,
        byte_range: Tuple[int, int],
        line_range: Optional[Tuple[int, int]] = None,
        license_concluded: Optional[Union[LicenseExpression, SpdxNoAssertion, SpdxNone]] = None,
        license_info_in_snippet: List[Union[LicenseExpression, SpdxNoAssertion, SpdxNone]] = None,
        license_comment: Optional[str] = None,
        copyright_text: Optional[Union[str, SpdxNoAssertion, SpdxNone]] = None,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        attribution_texts: List[str] = None,
    ):
        attribution_texts = [] if attribution_texts is None else attribution_texts
        license_info_in_snippet = [] if license_info_in_snippet is None else license_info_in_snippet
        check_types_and_set_values(self, locals())
