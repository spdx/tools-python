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
from unittest import mock

from spdx3.bump_from_spdx2.package import bump_package
from spdx3.model.software.package import Package
from spdx3.payload import Payload

from tests.spdx.fixtures import package_fixture
from spdx.model.package import Package as Spdx2_Package


@mock.patch("spdx3.model.creation_information.CreationInformation")
def test_bump_package(creation_information):
    spdx2_package: Spdx2_Package = package_fixture()

    payload = Payload()
    bump_package(spdx2_package, payload, creation_information=creation_information)
    package = payload.get_element(package_fixture().spdx_id)
    assert isinstance(package, Package)

    assert package.spdx_id == "SPDXRef-Package"
