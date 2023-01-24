# Copyright (c) 2022 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List

import pytest

from spdx.model.package import ExternalPackageRef, ExternalPackageRefCategory
from spdx.validation.external_package_ref_validator import validate_external_package_ref
from spdx.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.spdx.fixtures import external_package_ref_fixture

@pytest.mark.parametrize("category, reference_type, locator",
                         [(ExternalPackageRefCategory.SECURITY, "cpe22Type", "cpe:/o:canonical:ubuntu_linux:10.04:-:lts"),
                          (ExternalPackageRefCategory.SECURITY, "cpe23Type", "cpe:2.3:o:canonical:ubuntu_linux:10.04:-:lts:*:*:*:*:*"),
                          (ExternalPackageRefCategory.SECURITY, "advisory", "https://nvd.nist.gov/vuln/detail/CVE-2020-28498"),
                          (ExternalPackageRefCategory.SECURITY, "fix", "https://github.com/indutny/elliptic/commit/441b7428"),
                          (ExternalPackageRefCategory.SECURITY, "swid", "swid:2df9de35-0aff-4a86-ace6-f7dddd1ade4c"),
                          (ExternalPackageRefCategory.PACKAGE_MANAGER, "maven-central", "org.apache.tomcat:tomcat:9.0.0.M4"),
                          (ExternalPackageRefCategory.PACKAGE_MANAGER, "npm", "http-server@0.3.0"),
                          (ExternalPackageRefCategory.PACKAGE_MANAGER, "nuget", "Microsoft.AspNet.MVC/5.0.0"),
                          (ExternalPackageRefCategory.PACKAGE_MANAGER, "bower", "modernizr#2.6.2"),
                          (ExternalPackageRefCategory.PACKAGE_MANAGER, "purl", "pkg:docker/debian@sha256:2f04d3d33b6027bb74ecc81397abe780649ec89f1a2af18d7022737d0482cefe"),
                          (ExternalPackageRefCategory.PERSISTENT_ID, "swh", "swh:1:cnt:94a9ed024d3859793618152ea559a168bbcbb5e2"),
                          (ExternalPackageRefCategory.PERSISTENT_ID, "swh", "swh:1:dir:d198bc9d7a6bcf6db04f476d29314f157507d505"),
                          (ExternalPackageRefCategory.PERSISTENT_ID, "swh", "swh:1:rev:309cf2674ee7a0749978cf8265ab91a60aea0f7d"),
                          (ExternalPackageRefCategory.PERSISTENT_ID, "swh", "swh:1:rel:22ece559cc7cc2364edc5e5593d63ae8bd229f9f"),
                          (ExternalPackageRefCategory.PERSISTENT_ID, "swh", "swh:1:snp:c7c108084bc0bf3d81436bf980b46e98bd338453"),
                          (ExternalPackageRefCategory.PERSISTENT_ID, "gitoid", "gitoid:blob:sha1:261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64"),
                          (ExternalPackageRefCategory.PERSISTENT_ID, "gitoid", "gitoid:blob:sha256:3557f7eb43c621c71483743d4b37059bb80933e7f71277c0c3b3846159d1f61c"),
                          (ExternalPackageRefCategory.OTHER, "some idstring", "#//string-withOUT!Spaces\\?")
                          ])
def test_valid_external_package_ref(category, reference_type, locator):
    external_package_ref = ExternalPackageRef(category, reference_type, locator, "externalPackageRef comment")
    validation_messages: List[ValidationMessage] = validate_external_package_ref(external_package_ref, "parent_id")

    assert validation_messages == []


@pytest.mark.parametrize("external_package_ref, expected_message",
                         [(external_package_ref_fixture(),
                           "TBD"),
                          ])
@pytest.mark.skip(
    "add tests once external package ref validation is implemented: https://github.com/spdx/tools-python/issues/373")
def test_invalid_external_package_ref(external_package_ref, expected_message):
    parent_id = "SPDXRef-Package"
    validation_messages: List[ValidationMessage] = validate_external_package_ref(external_package_ref, parent_id)

    expected = ValidationMessage(expected_message,
                                 ValidationContext(parent_id=parent_id,
                                                   element_type=SpdxElementType.EXTERNAL_PACKAGE_REF,
                                                   full_element=external_package_ref))

    assert validation_messages == [expected]
