# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest import mock

import pytest

from spdx_tools.spdx3.model.software import Sbom, SBOMType


@mock.patch("spdx_tools.spdx3.model.CreationInfo", autospec=True)
def test_correct_initialization(creation_info):
    sbom = Sbom(
        "SPDXRef-Sbom",
        creation_info=creation_info,
        element=["spdx_id1", "spdx_id2"],
        root_element=["spdx_id3"],
        sbom_type=[SBOMType.DESIGN],
    )

    assert sbom.spdx_id == "SPDXRef-Sbom"
    assert sbom.creation_info == creation_info
    assert sbom.element == ["spdx_id1", "spdx_id2"]
    assert sbom.root_element == ["spdx_id3"]
    assert sbom.sbom_type == [SBOMType.DESIGN]


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        Sbom(2, creation_info={"creation_info": [3, 4, 5]}, element=[], root_element=[])

    assert len(err.value.args[0]) == 2
    for error in err.value.args[0]:
        assert error.startswith("SetterError Sbom:")
