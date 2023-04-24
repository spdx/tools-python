# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime
from unittest import mock

import pytest

from spdx_tools.spdx3.model import Hash, HashAlgorithm
from spdx_tools.spdx3.model.build import Build


@mock.patch("spdx_tools.spdx3.model.CreationInformation", autospec=True)
def test_correct_initialization(creation_information):
    build = Build(
        "some_spdx_id",
        creation_information,
        build_type="build type",
        build_id="build id",
        config_source_entrypoint=["entrypoint"],
        config_source_uri=["uri"],
        config_source_digest=[Hash(HashAlgorithm.MD2, "abcdef")],
        parameters={"param1": "value1"},
        build_start=datetime(2023, 1, 1),
        build_end=datetime(2023, 2, 2),
        environment={"param2": "value2"},
    )

    assert build.build_type == "build type"
    assert build.build_id == "build id"
    assert build.config_source_entrypoint == ["entrypoint"]
    assert build.config_source_uri == ["uri"]
    assert build.config_source_digest == [Hash(HashAlgorithm.MD2, "abcdef")]
    assert build.parameters == {"param1": "value1"}
    assert build.build_start == datetime(2023, 1, 1)
    assert build.build_end == datetime(2023, 2, 2)
    assert build.environment == {"param2": "value2"}


@mock.patch("spdx_tools.spdx3.model.CreationInformation", autospec=True)
def test_invalid_initialization(creation_information):
    with pytest.raises(TypeError) as err:
        Build(
            "some_spdx_id",
            creation_information,
            build_type="build type",
            config_source_digest=["hash_value"],
        )

    assert err.value.args[0] == [
        (
            "SetterError Build: type of argument \"config_source_digest\"[0] must be spdx_tools.spdx3.model.hash.Hash;"
            " got str instead: ['hash_value']"
        )
    ]
