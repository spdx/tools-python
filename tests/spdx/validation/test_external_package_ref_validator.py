# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from typing import List

import pytest

from spdx_tools.spdx.model import ExternalPackageRef, ExternalPackageRefCategory
from spdx_tools.spdx.validation.external_package_ref_validator import (
    BOWER_REGEX,
    CPE22TYPE_REGEX,
    CPE23TYPE_REGEX,
    GITOID_REGEX,
    MAVEN_CENTRAL_REGEX,
    NPM_REGEX,
    NUGET_REGEX,
    PURL_REGEX,
    SWH_REGEX,
    validate_external_package_ref,
)
from spdx_tools.spdx.validation.validation_message import SpdxElementType, ValidationContext, ValidationMessage


@pytest.mark.parametrize(
    "category, reference_type, locator",
    [
        (ExternalPackageRefCategory.SECURITY, "cpe22Type", "cpe:/o:canonical:ubuntu_linux:10.04:-:lts"),
        (ExternalPackageRefCategory.SECURITY, "cpe23Type", "cpe:2.3:o:canonical:ubuntu_linux:10.04:-:lts:*:*:*:*:*"),
        (ExternalPackageRefCategory.SECURITY, "advisory", "https://nvd.nist.gov/vuln/detail/CVE-2020-28498"),
        (ExternalPackageRefCategory.SECURITY, "fix", "https://github.com/indutny/elliptic/commit/441b7428"),
        (
            ExternalPackageRefCategory.SECURITY,
            "url",
            "https://github.com/christianlundkvist/blog/blob/master/2020_05_26_secp256k1_twist_attacks/"
            "secp256k1_twist_attacks.md",
        ),
        (ExternalPackageRefCategory.SECURITY, "swid", "swid:2df9de35-0aff-4a86-ace6-f7dddd1ade4c"),
        (ExternalPackageRefCategory.PACKAGE_MANAGER, "maven-central", "org.apache.tomcat:tomcat:9.0.0.M4"),
        (ExternalPackageRefCategory.PACKAGE_MANAGER, "npm", "http-server@0.3.0"),
        (ExternalPackageRefCategory.PACKAGE_MANAGER, "nuget", "Microsoft.AspNet.MVC/5.0.0"),
        (ExternalPackageRefCategory.PACKAGE_MANAGER, "bower", "modernizr#2.6.2"),
        (
            ExternalPackageRefCategory.PACKAGE_MANAGER,
            "purl",
            "pkg:docker/debian@sha256:2f04d3d33b6027bb74ecc81397abe780649ec89f1a2af18d7022737d0482cefe",
        ),
        (
            ExternalPackageRefCategory.PACKAGE_MANAGER,
            "purl",
            "pkg:bitbucket/birkenfeld/pygments-main@244fd47e07d1014f0aed9c",
        ),
        (ExternalPackageRefCategory.PACKAGE_MANAGER, "purl", "pkg:deb/debian/curl@7.50.3-1?arch=i386&distro=jessie"),
        (
            ExternalPackageRefCategory.PACKAGE_MANAGER,
            "purl",
            "pkg:docker/customer/dockerimage@sha256:244fd47e07d1004f0aed9c?repository_url=gcr.io",
        ),
        (ExternalPackageRefCategory.PACKAGE_MANAGER, "purl", "pkg:gem/jruby-launcher@1.1.2?platform=java"),
        (ExternalPackageRefCategory.PACKAGE_MANAGER, "purl", "pkg:gem/ruby-advisory-db-check@0.12.4"),
        (
            ExternalPackageRefCategory.PACKAGE_MANAGER,
            "purl",
            "pkg:github/package-url/purl-spec@244fd47e07d1004f0aed9c",
        ),
        (
            ExternalPackageRefCategory.PACKAGE_MANAGER,
            "purl",
            "pkg:golang/google.golang.org/genproto#googleapis/api/annotations",
        ),
        (
            ExternalPackageRefCategory.PACKAGE_MANAGER,
            "purl",
            "pkg:maven/org.apache.xmlgraphics/batik-anim@1.9.1?repository_url=repo.spring.io%2Frelease",
        ),
        (ExternalPackageRefCategory.PACKAGE_MANAGER, "purl", "pkg:npm/%40angular/animation@12.3.1"),
        (ExternalPackageRefCategory.PACKAGE_MANAGER, "purl", "pkg:nuget/EnterpriseLibrary.Common@6.0.1304"),
        (
            ExternalPackageRefCategory.PACKAGE_MANAGER,
            "purl",
            "pkg:rpm/fedora/curl@7.50.3-1.fc25?arch=i386&distro=fedora-25",
        ),
        (ExternalPackageRefCategory.PERSISTENT_ID, "swh", "swh:1:cnt:94a9ed024d3859793618152ea559a168bbcbb5e2"),
        (ExternalPackageRefCategory.PERSISTENT_ID, "swh", "swh:1:dir:d198bc9d7a6bcf6db04f476d29314f157507d505"),
        (ExternalPackageRefCategory.PERSISTENT_ID, "swh", "swh:1:rev:309cf2674ee7a0749978cf8265ab91a60aea0f7d"),
        (ExternalPackageRefCategory.PERSISTENT_ID, "swh", "swh:1:rel:22ece559cc7cc2364edc5e5593d63ae8bd229f9f"),
        (ExternalPackageRefCategory.PERSISTENT_ID, "swh", "swh:1:snp:c7c108084bc0bf3d81436bf980b46e98bd338453"),
        (
            ExternalPackageRefCategory.PERSISTENT_ID,
            "gitoid",
            "gitoid:blob:sha1:261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64",
        ),
        (
            ExternalPackageRefCategory.PERSISTENT_ID,
            "gitoid",
            "gitoid:blob:sha256:3557f7eb43c621c71483743d4b37059bb80933e7f71277c0c3b3846159d1f61c",
        ),
        (ExternalPackageRefCategory.OTHER, "some idstring", "#//string-withOUT!Spaces\\?"),
    ],
)
def test_valid_external_package_ref(category, reference_type, locator):
    external_package_ref = ExternalPackageRef(category, reference_type, locator, "externalPackageRef comment")
    validation_messages: List[ValidationMessage] = validate_external_package_ref(
        external_package_ref, "parent_id", "SPDX-2.3"
    )

    assert validation_messages == []


@pytest.mark.parametrize(
    "category, reference_type, locator, expected_message",
    [
        (
            ExternalPackageRefCategory.SECURITY,
            "cpe22Typo",
            "cpe:/o:canonical:ubuntu_linux:10.04:-:lts",
            "externalPackageRef type in category SECURITY must be one of ['cpe22Type', 'cpe23Type', 'advisory', 'fix'"
            ", 'url', 'swid'], but is: cpe22Typo",
        ),
        (
            ExternalPackageRefCategory.PACKAGE_MANAGER,
            "nugat",
            "cpe:/o:canonical:ubuntu_linux:10.04:-:lts",
            "externalPackageRef type in category PACKAGE_MANAGER must be one of ['maven-central', 'npm', 'nuget',"
            " 'bower', 'purl'], but is: nugat",
        ),
        (
            ExternalPackageRefCategory.PERSISTENT_ID,
            "git-oid",
            "cpe:/o:canonical:ubuntu_linux:10.04:-:lts",
            "externalPackageRef type in category PERSISTENT_ID must be one of ['swh', 'gitoid'], but is: git-oid",
        ),
    ],
)
def test_invalid_external_package_ref_types(category, reference_type, locator, expected_message):
    external_package_ref = ExternalPackageRef(category, reference_type, locator, "externalPackageRef comment")
    parent_id = "SPDXRef-Package"
    validation_messages: List[ValidationMessage] = validate_external_package_ref(
        external_package_ref, parent_id, "SPDX-2.3"
    )

    expected = ValidationMessage(
        expected_message,
        ValidationContext(
            parent_id=parent_id, element_type=SpdxElementType.EXTERNAL_PACKAGE_REF, full_element=external_package_ref
        ),
    )

    assert validation_messages == [expected]


@pytest.mark.parametrize(
    "category, reference_type, locator, expected_message",
    [
        (
            ExternalPackageRefCategory.SECURITY,
            "cpe22Type",
            "cpe:o:canonical:ubuntu_linux:10.04:-:lts",
            f'externalPackageRef locator of type "cpe22Type" must conform with the regex {CPE22TYPE_REGEX}, but is: '
            f"cpe:o:canonical:ubuntu_linux:10.04:-:lts",
        ),
        (
            ExternalPackageRefCategory.SECURITY,
            "cpe23Type",
            "cpe:2.3:/o:canonical:ubuntu_linux:10.04:-:lts:*:*:*:*:*",
            f'externalPackageRef locator of type "cpe23Type" must conform with the regex {CPE23TYPE_REGEX}, but is: '
            f"cpe:2.3:/o:canonical:ubuntu_linux:10.04:-:lts:*:*:*:*:*",
        ),
        (
            ExternalPackageRefCategory.SECURITY,
            "advisory",
            "http://locatorurl",
            'externalPackageRef locator of type "advisory" must be a valid URL, but is: http://locatorurl',
        ),
        (
            ExternalPackageRefCategory.SECURITY,
            "fix",
            "http://fixurl",
            'externalPackageRef locator of type "fix" must be a valid URL, but is: http://fixurl',
        ),
        (
            ExternalPackageRefCategory.SECURITY,
            "url",
            "http://url",
            'externalPackageRef locator of type "url" must be a valid URL, but is: http://url',
        ),
        (
            ExternalPackageRefCategory.SECURITY,
            "swid",
            "2df9de35-0aff-4a86-ace6-f7dddd1ade4c",
            'externalPackageRef locator of type "swid" must be a valid URI with scheme swid, but is: '
            "2df9de35-0aff-4a86-ace6-f7dddd1ade4c",
        ),
        (
            ExternalPackageRefCategory.PACKAGE_MANAGER,
            "maven-central",
            "org.apache.tomcat:tomcat:tomcat:9.0.0.M4",
            f'externalPackageRef locator of type "maven-central" must conform with the regex {MAVEN_CENTRAL_REGEX}, '
            f"but is: org.apache.tomcat:tomcat:tomcat:9.0.0.M4",
        ),
        (
            ExternalPackageRefCategory.PACKAGE_MANAGER,
            "npm",
            "http-server:0.3.0",
            f'externalPackageRef locator of type "npm" must conform with the regex {NPM_REGEX}, '
            f"but is: http-server:0.3.0",
        ),
        (
            ExternalPackageRefCategory.PACKAGE_MANAGER,
            "nuget",
            "Microsoft.AspNet.MVC@5.0.0",
            f'externalPackageRef locator of type "nuget" must conform with the regex {NUGET_REGEX}, '
            f"but is: Microsoft.AspNet.MVC@5.0.0",
        ),
        (
            ExternalPackageRefCategory.PACKAGE_MANAGER,
            "bower",
            "modernizr:2.6.2",
            f'externalPackageRef locator of type "bower" must conform with the regex {BOWER_REGEX}, '
            f"but is: modernizr:2.6.2",
        ),
        (
            ExternalPackageRefCategory.PACKAGE_MANAGER,
            "purl",
            "pkg:npm@12.3.1",
            f'externalPackageRef locator of type "purl" must conform with the regex {PURL_REGEX}, '
            f"but is: pkg:npm@12.3.1",
        ),
        (
            ExternalPackageRefCategory.PERSISTENT_ID,
            "swh",
            "swh:cnt:94a9ed024d3859793618152ea559a168bbcbb5e2",
            f'externalPackageRef locator of type "swh" must conform with the regex {SWH_REGEX}, '
            f"but is: swh:cnt:94a9ed024d3859793618152ea559a168bbcbb5e2",
        ),
        (
            ExternalPackageRefCategory.PERSISTENT_ID,
            "gitoid",
            "gitoid:blob:sha1:3557f7eb43c621c71483743d4b37059bb80933e7f71277c0c3b3846159d1f61c",
            f'externalPackageRef locator of type "gitoid" must conform with the regex {GITOID_REGEX}, '
            f"but is: gitoid:blob:sha1:3557f7eb43c621c71483743d4b37059bb80933e7f71277c0c3b3846159d1f61c",
        ),
        (
            ExternalPackageRefCategory.PERSISTENT_ID,
            "gitoid",
            "gitoid:blob:sha256:261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64",
            f'externalPackageRef locator of type "gitoid" must conform with the regex {GITOID_REGEX},'
            f" but is: gitoid:blob:sha256:261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64",
        ),
        (
            ExternalPackageRefCategory.OTHER,
            "id string",
            "locator string",
            "externalPackageRef locator in category OTHER must contain no spaces, but is: locator string",
        ),
    ],
)
def test_invalid_external_package_ref_locators(category, reference_type, locator, expected_message):
    external_package_ref = ExternalPackageRef(category, reference_type, locator, "externalPackageRef comment")
    parent_id = "SPDXRef-Package"
    validation_messages: List[ValidationMessage] = validate_external_package_ref(
        external_package_ref, parent_id, "SPDX-2.3"
    )

    expected = ValidationMessage(
        expected_message,
        ValidationContext(
            parent_id=parent_id, element_type=SpdxElementType.EXTERNAL_PACKAGE_REF, full_element=external_package_ref
        ),
    )

    assert validation_messages == [expected]


@pytest.mark.parametrize(
    "category, reference_type, locator",
    [
        (ExternalPackageRefCategory.SECURITY, "advisory", "https://nvd.nist.gov/vuln/detail/CVE-2020-28498"),
        (ExternalPackageRefCategory.SECURITY, "fix", "https://github.com/indutny/elliptic/commit/441b7428"),
        (
            ExternalPackageRefCategory.SECURITY,
            "url",
            "https://github.com/christianlundkvist/blog/blob/master/2020_05_26_secp256k1_twist_attacks/"
            "secp256k1_twist_attacks.md",
        ),
        (ExternalPackageRefCategory.SECURITY, "swid", "swid:2df9de35-0aff-4a86-ace6-f7dddd1ade4c"),
    ],
)
def test_v2_3only_external_package_ref_types(category, reference_type, locator):
    external_package_ref = ExternalPackageRef(category, reference_type, locator, "externalPackageRef comment")
    parent_id = "SPDXRef-Package"
    validation_messages: List[ValidationMessage] = validate_external_package_ref(
        external_package_ref, parent_id, "SPDX-2.2"
    )

    expected = ValidationMessage(
        f'externalPackageRef type "{reference_type}" is not supported in SPDX-2.2',
        ValidationContext(
            parent_id=parent_id, element_type=SpdxElementType.EXTERNAL_PACKAGE_REF, full_element=external_package_ref
        ),
    )

    assert validation_messages == [expected]
