# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime

import pytest
from semantic_version import Version

from spdx_tools.spdx3.model import CreationInfo, ProfileIdentifierType
from tests.spdx3.fixtures import creation_info_fixture
from tests.spdx3.model.model_test_utils import get_property_names


def test_correct_initialization():
    creation_info = creation_info_fixture()

    for property_name in get_property_names(CreationInfo):
        assert getattr(creation_info, property_name) is not None

    assert creation_info.spec_version == Version("3.0.0")
    assert creation_info.created == datetime(2022, 12, 1)
    assert creation_info.created_by == ["https://spdx.test/tools-python/creation_info_created_by"]
    assert creation_info.created_using == ["https://spdx.test/tools-python/creation_info_created_using"]
    assert creation_info.profile == [
        ProfileIdentifierType.CORE,
        ProfileIdentifierType.SOFTWARE,
        ProfileIdentifierType.LICENSING,
    ]
    assert creation_info.data_license == "CC0-1.0"
    assert creation_info.comment == "creationInfoComment"


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        CreationInfo("2.3", "2012-01-01", [], "core", 3, [], [])

    assert len(err.value.args[0]) == 5
    for error in err.value.args[0]:
        assert error.startswith("SetterError CreationInfo:")


def test_incomplete_initialization():
    with pytest.raises(TypeError) as err:
        CreationInfo("2.3")

    assert (
        "__init__() missing 3 required positional arguments: 'created', 'created_by', and 'profile'"
        in err.value.args[0]
    )
