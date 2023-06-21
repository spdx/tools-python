# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx3.model import ExternalReference, ExternalReferenceType
from tests.spdx3.fixtures import external_reference_fixture
from tests.spdx3.model.model_test_utils import get_property_names


def test_correct_initialization():
    external_reference = external_reference_fixture()

    for property_name in get_property_names(ExternalReference):
        assert getattr(external_reference, property_name) is not None

    assert external_reference.external_reference_type == ExternalReferenceType.OTHER
    assert external_reference.locator == ["org.apache.tomcat:tomcat:9.0.0.M4"]
    assert external_reference.content_type == "externalReferenceContentType"
    assert external_reference.comment == "externalReferenceComment"


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        ExternalReference("OTHER", "a URI", 34, True)

    assert len(err.value.args[0]) == 4
    for error in err.value.args[0]:
        assert error.startswith("SetterError ExternalReference:")
