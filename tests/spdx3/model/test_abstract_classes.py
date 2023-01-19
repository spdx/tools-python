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
import pytest

from spdx3.model.artifact import Artifact
from spdx3.model.element import Element
from spdx3.model.integrity_method import IntegrityMethod
from spdx3.model.spdx_collection import SpdxCollection


@pytest.mark.parametrize("abstract_class", [Element, Artifact, SpdxCollection, IntegrityMethod])
def test_initialization_throws_error(abstract_class):
    with pytest.raises(TypeError) as err:
        abstract_class()

    assert f"Can't instantiate abstract class {abstract_class.__name__}" in err.value.args[0]
