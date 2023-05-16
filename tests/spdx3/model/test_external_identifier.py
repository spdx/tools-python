# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest import TestCase

import pytest

from spdx_tools.spdx3.model import ExternalIdentifier, ExternalIdentifierType


def test_correct_initialization():
    external_identifier = ExternalIdentifier(
        ExternalIdentifierType.CPE22,
        "cpe:/o:canonical:ubuntu_linux:10.04:-:lts",
        "This is a comment",
        ["first locator", "second locator"],
        "authority",
    )
    assert external_identifier.external_identifier_type == ExternalIdentifierType.CPE22
    assert external_identifier.identifier == "cpe:/o:canonical:ubuntu_linux:10.04:-:lts"
    assert external_identifier.comment == "This is a comment"
    TestCase().assertCountEqual(external_identifier.identifier_locator, ["first locator", "second locator"])
    assert external_identifier.issuing_authority == "authority"


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        ExternalIdentifier("CPE22", ["identifier", "another_identifier"], 34, "locator", True)

    assert len(err.value.args[0]) == 5
    for error in err.value.args[0]:
        assert error.startswith("SetterError ExternalIdentifier:")
