# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from datetime import datetime
from unittest import mock

import pytest
from license_expression import LicenseExpression, Licensing

from spdx_tools.spdx.model import Checksum, ChecksumAlgorithm, Package, PackagePurpose, SpdxNoAssertion, SpdxNone


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


def test_wrong_type_in_spdx_id():
    with pytest.raises(TypeError):
        Package(42, "name", "location")


def test_wrong_type_in_name():
    with pytest.raises(TypeError):
        Package("id", 42, "location")


def test_wrong_type_in_download_location():
    with pytest.raises(TypeError):
        Package("id", "name", 42)


def test_wrong_type_in_version():
    with pytest.raises(TypeError):
        Package("id", "name", "location", version=42)


def test_wrong_type_in_file_name():
    with pytest.raises(TypeError):
        Package("id", "name", "location", file_name=42)


def test_wrong_type_in_supplier():
    with pytest.raises(TypeError):
        Package("id", "name", "location", supplier=SpdxNone())


def test_wrong_type_in_originator():
    with pytest.raises(TypeError):
        Package("id", "name", "location", originator=SpdxNone())


def test_wrong_type_in_files_analyzed():
    with pytest.raises(TypeError):
        Package("id", "name", "location", files_analyzed=None)


def test_wrong_type_in_verification_code():
    with pytest.raises(TypeError):
        Package("id", "name", "location", verification_code=[])


def test_wrong_type_in_checksums():
    with pytest.raises(TypeError):
        Package("id", "name", "location", checksums=Checksum(ChecksumAlgorithm.MD2, "value"))


def test_wrong_type_in_homepage():
    with pytest.raises(TypeError):
        Package("id", "name", "location", homepage=42)


def test_wrong_type_in_source_info():
    with pytest.raises(TypeError):
        Package("id", "name", "location", source_info=42)


def test_wrong_type_in_license_concluded():
    with pytest.raises(TypeError):
        Package("id", "name", "location", license_concluded=[])


def test_wrong_type_in_license_info_from_files():
    with pytest.raises(TypeError):
        Package("id", "name", "location", license_info_from_files=LicenseExpression("string"))


def test_wrong_type_in_license_declared():
    with pytest.raises(TypeError):
        Package("id", "name", "location", license_declared=[])


def test_wrong_type_in_license_comment():
    with pytest.raises(TypeError):
        Package("id", "name", "location", license_comment=42)


def test_wrong_type_in_copyright_text():
    with pytest.raises(TypeError):
        Package("id", "name", "location", copyright_text=42)


def test_wrong_type_in_summary():
    with pytest.raises(TypeError):
        Package("id", "name", "location", summary=42)


def test_wrong_type_in_description():
    with pytest.raises(TypeError):
        Package("id", "name", "location", description=42)


def test_wrong_type_in_comment():
    with pytest.raises(TypeError):
        Package("id", "name", "location", comment=[])


def test_wrong_type_in_external_references():
    with pytest.raises(TypeError):
        Package("id", "name", "location", external_references=["external_ref"])


def test_wrong_type_in_attribution_texts():
    with pytest.raises(TypeError):
        Package("id", "name", "location", attribution_texts="text")


def test_wrong_type_in_primary_package_purpose():
    with pytest.raises(TypeError):
        Package("id", "name", "location", primary_package_purpose=[])


def test_wrong_type_in_release_date():
    with pytest.raises(TypeError):
        Package("id", "name", "location", release_date=42)


def test_wrong_type_in_built_date():
    with pytest.raises(TypeError):
        Package("id", "name", "location", built_date="2022-01-01")


def test_wrong_type_in_valid_until_date():
    with pytest.raises(TypeError):
        Package("id", "name", "location", valid_until_date=SpdxNone())
