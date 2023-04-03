# SPDX-FileCopyrightText: 2023 spdx contributors

# SPDX-License-Identifier: Apache-2.0
from unittest import mock

import pytest

from spdx3.model.software.sbom import Sbom


@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_correct_initialization(creation_information):
    sbom = Sbom("SPDXRef-Sbom", creation_information, elements=["spdx_id1", "spdx_id2"], root_elements=["spdx_id3"])

    assert sbom.spdx_id == "SPDXRef-Sbom"
    assert sbom.creation_info == creation_information
    assert sbom.elements == ["spdx_id1", "spdx_id2"]
    assert sbom.root_elements == ["spdx_id3"]


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        Sbom(2, {"creation_info": [3, 4, 5]}, elements=[], root_elements=[])

    assert err.value.args[0] == [
        'SetterError Sbom: type of argument "spdx_id" must be str; got int instead: 2',
        'SetterError Sbom: type of argument "creation_info" must be '
        "spdx3.model.creation_information.CreationInformation; got dict instead: "
        "{'creation_info': [3, 4, 5]}",
    ]
