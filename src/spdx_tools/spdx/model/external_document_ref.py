# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx.model import Checksum


@dataclass_with_properties
class ExternalDocumentRef:
    document_ref_id: str  # of the form "DocumentRef-[idstring]"
    document_uri: str
    checksum: Checksum

    def __init__(self, document_ref_id: str, document_uri: str, checksum: Checksum):
        check_types_and_set_values(self, locals())
