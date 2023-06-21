# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx3.model import ExternalIdentifier, ExternalIdentifierType
from tests.spdx3.fixtures import external_identifier_fixture
from tests.spdx3.model.model_test_utils import get_property_names


def test_correct_initialization():
    external_identifier = external_identifier_fixture()

    for property_name in get_property_names(ExternalIdentifier):
        assert getattr(external_identifier, property_name) is not None

    assert external_identifier.external_identifier_type == ExternalIdentifierType.OTHER
    assert external_identifier.identifier == "externalIdentifierIdentifier"
    assert external_identifier.comment == "externalIdentifierComment"
    assert external_identifier.identifier_locator == [
        "https://spdx.test/tools-python/external_identifier_identifier_locator"
    ]
    assert (
        external_identifier.issuing_authority == "https://spdx.test/tools-python/external_identifier_issuing_authority"
    )


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        ExternalIdentifier("CPE22", ["identifier", "another_identifier"], 34, "locator", True)

    assert len(err.value.args[0]) == 5
    for error in err.value.args[0]:
        assert error.startswith("SetterError ExternalIdentifier:")
