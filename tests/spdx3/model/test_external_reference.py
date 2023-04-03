# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx3.model.external_reference import ExternalReference, ExternalReferenceType


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

    assert err.value.args[0] == [
        'SetterError ExternalReference: type of argument "external_reference_type" '
        "must be one of (spdx3.model.external_reference.ExternalReferenceType, "
        "NoneType); got str instead: OTHER",
        'SetterError ExternalReference: type of argument "locator" must be a list; ' "got str instead: a URI",
        'SetterError ExternalReference: type of argument "content_type" must be one '
        "of (str, NoneType); got int instead: 34",
        'SetterError ExternalReference: type of argument "comment" must be one of '
        "(str, NoneType); got bool instead: True",
    ]
