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

    assert err.value.args[0] == [
        'SetterError ExternalIdentifier: type of argument "external_identifier_type" '
        "must be spdx_tools.spdx3.model.external_identifier.ExternalIdentifierType; got str "
        "instead: CPE22",
        'SetterError ExternalIdentifier: type of argument "identifier" must be str; '
        "got list instead: ['identifier', 'another_identifier']",
        'SetterError ExternalIdentifier: type of argument "comment" must be one of '
        "(str, NoneType); got int instead: 34",
        'SetterError ExternalIdentifier: type of argument "identifier_locator" must '
        "be a list; got str instead: locator",
        'SetterError ExternalIdentifier: type of argument "issuing_authority" must be '
        "one of (str, NoneType); got bool instead: True",
    ]
