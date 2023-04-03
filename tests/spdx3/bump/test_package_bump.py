# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest import mock

from spdx3.bump_from_spdx2.package import bump_package
from spdx3.model.software.package import Package
from spdx3.payload import Payload
from spdx.model.package import Package as Spdx2_Package
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
    assert package.package_version == spdx2_package.version
