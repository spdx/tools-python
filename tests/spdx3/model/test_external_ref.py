# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx3.model.core import ExternalRef, ExternalRefType
from tests.spdx3.fixtures import external_ref_fixture
from tests.spdx3.model.model_test_utils import get_property_names


def test_correct_initialization():
    external_ref = external_ref_fixture()

    for property_name in get_property_names(ExternalRef):
        assert getattr(external_ref, property_name) is not None

    assert external_ref.external_ref_type == ExternalRefType.OTHER
    assert external_ref.locator == ["org.apache.tomcat:tomcat:9.0.0.M4"]
    assert external_ref.content_type == "externalRefContentType"
    assert external_ref.comment == "externalRefComment"


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        ExternalRef("OTHER", "a URI", 34, True)

    assert len(err.value.args[0]) == 4
    for error in err.value.args[0]:
        assert error.startswith("SetterError ExternalRef:")
