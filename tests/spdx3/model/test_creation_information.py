# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from datetime import datetime

import pytest
from semantic_version import Version

from spdx3.model.creation_information import CreationInformation


def test_correct_initialization():
    creation_information = CreationInformation(
        Version("3.0.0"), datetime(2023, 1, 11, 16, 21), [], [], ["core", "software"], "CC0"
    )

    assert creation_information.spec_version == Version("3.0.0")
    assert creation_information.created == datetime(2023, 1, 11, 16, 21)
    assert creation_information.created_by == []
    assert creation_information.created_using == []
    assert creation_information.profile == ["core", "software"]
    assert creation_information.data_license == "CC0"


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        CreationInformation("2.3", "2012-01-01", [], [], "core", 3)

    assert err.value.args[0] == [
        'SetterError CreationInformation: type of argument "spec_version" must be '
        "semantic_version.base.Version; got str instead: 2.3",
        'SetterError CreationInformation: type of argument "created" must be '
        "datetime.datetime; got str instead: 2012-01-01",
        'SetterError CreationInformation: type of argument "profile" must be a list; ' "got str instead: core",
        'SetterError CreationInformation: type of argument "data_license" must be ' "str; got int instead: 3",
    ]


def test_incomplete_initialization():
    with pytest.raises(TypeError) as err:
        CreationInformation("2.3")

    assert (
        "__init__() missing 4 required positional arguments: 'created', 'created_by', 'created_using', and 'profile'"
        in err.value.args[0]
    )
