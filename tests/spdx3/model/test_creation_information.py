# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime

import pytest
from semantic_version import Version

from spdx_tools.spdx3.model import CreationInformation, ProfileIdentifier


def test_correct_initialization():
    creation_information = CreationInformation(
        Version("3.0.0"),
        datetime(2023, 1, 11, 16, 21),
        [],
        [],
        [ProfileIdentifier.CORE, ProfileIdentifier.SOFTWARE],
        "CC0",
        "some comment",
    )

    assert creation_information.spec_version == Version("3.0.0")
    assert creation_information.created == datetime(2023, 1, 11, 16, 21)
    assert creation_information.created_by == []
    assert creation_information.created_using == []
    assert creation_information.profile == [ProfileIdentifier.CORE, ProfileIdentifier.SOFTWARE]
    assert creation_information.data_license == "CC0"
    assert creation_information.comment == "some comment"


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        CreationInformation("2.3", "2012-01-01", [], [], "core", 3, [])

    assert err.value.args[0] == [
        'SetterError CreationInformation: type of argument "spec_version" must be '
        "semantic_version.base.Version; got str instead: 2.3",
        'SetterError CreationInformation: type of argument "created" must be '
        "datetime.datetime; got str instead: 2012-01-01",
        'SetterError CreationInformation: type of argument "profile" must be a list; ' "got str instead: core",
        'SetterError CreationInformation: type of argument "data_license" must be ' "str; got int instead: 3",
        'SetterError CreationInformation: type of argument "comment" must be'
        " one of (str, NoneType); got list instead: []",
    ]


def test_incomplete_initialization():
    with pytest.raises(TypeError) as err:
        CreationInformation("2.3")

    assert (
        "__init__() missing 4 required positional arguments: 'created', 'created_by', 'created_using', and 'profile'"
        in err.value.args[0]
    )
