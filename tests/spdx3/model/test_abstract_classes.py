# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx3.model.artifact import Artifact
from spdx_tools.spdx3.model.element import Element
from spdx_tools.spdx3.model.integrity_method import IntegrityMethod
from spdx_tools.spdx3.model.spdx_collection import SpdxCollection


@pytest.mark.parametrize("abstract_class", [Element, Artifact, SpdxCollection, IntegrityMethod])
def test_initialization_throws_error(abstract_class):
    with pytest.raises(TypeError) as err:
        abstract_class()

    assert f"Can't instantiate abstract class {abstract_class.__name__}" in err.value.args[0]
