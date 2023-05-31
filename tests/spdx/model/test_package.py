# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from datetime import datetime
from unittest import mock

from license_expression import Licensing

from spdx_tools.spdx.model import Package, PackagePurpose, SpdxNoAssertion, SpdxNone


@mock.patch("spdx_tools.spdx.model.ExternalPackageRef", autospec=True)
@mock.patch("spdx_tools.spdx.model.Checksum", autospec=True)
@mock.patch("spdx_tools.spdx.model.PackageVerificationCode", autospec=True)
@mock.patch("spdx_tools.spdx.model.Actor", autospec=True)
def test_correct_initialization(actor, verif_code, checksum, ext_ref):
    package = Package(
        "id",
        "name",
        SpdxNoAssertion(),
        "version",
        "file_name",
        SpdxNoAssertion(),
        actor,
        True,
        verif_code,
        [checksum],
        "homepage",
        "source_info",
        None,
        [Licensing().parse("license and expression"), SpdxNoAssertion()],
        SpdxNone(),
        "comment on license",
        "copyright",
        "summary",
        "description",
        "comment",
        [ext_ref, ext_ref],
        ["text"],
        PackagePurpose.OTHER,
        datetime(2022, 1, 1),
        None,
        None,
    )
    assert package.spdx_id == "id"
    assert package.name == "name"
    assert package.download_location == SpdxNoAssertion()
    assert package.version == "version"
    assert package.file_name == "file_name"
    assert package.supplier == SpdxNoAssertion()
    assert package.originator == actor
    assert package.files_analyzed
    assert package.verification_code == verif_code
    assert package.checksums == [checksum]
    assert package.homepage == "homepage"
    assert package.source_info == "source_info"
    assert package.license_concluded is None
    assert package.license_info_from_files == [Licensing().parse("license and expression"), SpdxNoAssertion()]
    assert package.license_declared == SpdxNone()
    assert package.license_comment == "comment on license"
    assert package.copyright_text == "copyright"
    assert package.summary == "summary"
    assert package.description == "description"
    assert package.comment == "comment"
    assert package.external_references == [ext_ref, ext_ref]
    assert package.attribution_texts == ["text"]
    assert package.primary_package_purpose == PackagePurpose.OTHER
    assert package.release_date == datetime(2022, 1, 1)
    assert package.built_date is None
    assert package.valid_until_date is None


def test_correct_initialization_with_default_values():
    package = Package("id", "name", "location")
    assert package.spdx_id == "id"
    assert package.name == "name"
    assert package.download_location == "location"
    assert package.version is None
    assert package.file_name is None
    assert package.supplier is None
    assert package.originator is None
    assert package.files_analyzed
    assert package.verification_code is None
    assert package.checksums == []
    assert package.homepage is None
    assert package.source_info is None
    assert package.license_concluded is None
    assert package.license_info_from_files == []
    assert package.license_declared is None
    assert package.license_comment is None
    assert package.copyright_text is None
    assert package.summary is None
    assert package.description is None
    assert package.comment is None
    assert package.external_references == []
    assert package.attribution_texts == []
    assert package.primary_package_purpose is None
    assert package.release_date is None
    assert package.built_date is None
    assert package.valid_until_date is None
