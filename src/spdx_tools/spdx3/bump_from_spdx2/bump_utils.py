# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import Optional, Union

from spdx_tools.spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx_tools.spdx.model.spdx_none import SpdxNone


def handle_no_assertion_or_none(field: Union[SpdxNone, SpdxNoAssertion, str], field_name: str) -> Optional[str]:
    if isinstance(field, SpdxNone):
        print(f"{field_name}: Missing conversion for SpdxNone.")
        return None
    if isinstance(field, SpdxNoAssertion):
        return None
    if isinstance(field, str):
        return field
