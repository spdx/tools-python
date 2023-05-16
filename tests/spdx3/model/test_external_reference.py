# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx3.model import ExternalReference, ExternalReferenceType


def test_correct_initialization():
    external_reference = ExternalReference(
        ExternalReferenceType.SECURITY_ADVISORY, ["https://anyURI"], "MediaType", "This is a comment"
    )
    assert external_reference.external_reference_type == ExternalReferenceType.SECURITY_ADVISORY
    assert external_reference.locator == ["https://anyURI"]
    assert external_reference.content_type == "MediaType"
    assert external_reference.comment == "This is a comment"


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        ExternalReference("OTHER", "a URI", 34, True)

    assert len(err.value.args[0]) == 4
    for error in err.value.args[0]:
        assert error.startswith("SetterError ExternalReference:")
