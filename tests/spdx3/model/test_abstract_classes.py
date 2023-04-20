# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx3.model import Artifact, Element, IntegrityMethod, SpdxCollection


@pytest.mark.parametrize("abstract_class", [Element, Artifact, SpdxCollection, IntegrityMethod])
def test_initialization_throws_error(abstract_class):
    with pytest.raises(TypeError) as err:
        abstract_class()

    assert f"Can't instantiate abstract class {abstract_class.__name__}" in err.value.args[0]
