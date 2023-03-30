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

from spdx.model.package import Package as Spdx2_Package
from spdx3.bump_from_spdx2.package import bump_package
from spdx3.model.software.package import Package
from spdx3.payload import Payload
from tests.spdx.fixtures import package_fixture


@mock.patch("spdx3.model.creation_information.CreationInformation")
def test_bump_package(creation_information):
    payload = Payload()
    document_namespace = "https://doc.namespace"
    spdx2_package: Spdx2_Package = package_fixture()
    expected_new_package_id = f"{document_namespace}#{spdx2_package.spdx_id}"

    bump_package(spdx2_package, payload, creation_information, document_namespace)
    package = payload.get_element(expected_new_package_id)

    assert isinstance(package, Package)
    assert package.spdx_id == expected_new_package_id
