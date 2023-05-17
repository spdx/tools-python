# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime

import pytest
from semantic_version import Version

from spdx_tools.spdx3.model import CreationInformation, ProfileIdentifier
from tests.spdx3.fixtures import creation_info_fixture
from tests.spdx3.model.model_test_utils import get_property_names


def test_correct_initialization():
    creation_information = creation_info_fixture()

    for property_name in get_property_names(CreationInformation):
        assert getattr(creation_information, property_name) is not None

    assert creation_information.spec_version == Version("3.0.0")
    assert creation_information.created == datetime(2022, 12, 1)
    assert creation_information.created_by == ["https://spdx.test/tools-python/creation_info_created_by"]
    assert creation_information.created_using == ["https://spdx.test/tools-python/creation_info_created_using"]
    assert creation_information.profile == [
        ProfileIdentifier.CORE,
        ProfileIdentifier.SOFTWARE,
        ProfileIdentifier.LICENSING,
    ]
    assert creation_information.data_license == "CC0-1.0"
    assert creation_information.comment == "creationInfoComment"


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        CreationInformation("2.3", "2012-01-01", [], [], "core", 3, [])

    assert len(err.value.args[0]) == 5
    for error in err.value.args[0]:
        assert error.startswith("SetterError CreationInformation:")


def test_incomplete_initialization():
    with pytest.raises(TypeError) as err:
        CreationInformation("2.3")

    assert (
        "__init__() missing 4 required positional arguments: 'created', 'created_by', 'created_using', and 'profile'"
        in err.value.args[0]
    )
