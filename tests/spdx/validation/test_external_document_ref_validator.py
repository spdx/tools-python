# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from typing import List

from spdx_tools.spdx.validation.external_document_ref_validator import validate_external_document_ref
from spdx_tools.spdx.validation.validation_message import ValidationMessage
from tests.spdx.fixtures import external_document_ref_fixture


def test_valid_external_document_ref():
    external_document_ref = external_document_ref_fixture()
    validation_messages: List[ValidationMessage] = validate_external_document_ref(
        external_document_ref, "parent_id", "SPDX-2.3"
    )

    assert validation_messages == []
