#  Copyright (c) 2022 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from datetime import datetime
from unittest import mock
from unittest.mock import MagicMock

import pytest

from src.jsonschema.package_converter import PackageConverter
from src.jsonschema.package_properties import PackageProperty
from src.model.actor import Actor, ActorType
from src.model.annotation import Annotation, AnnotationType
from src.model.checksum import Checksum, ChecksumAlgorithm
from src.model.document import Document
from src.model.license_expression import LicenseExpression
from src.model.package import Package, PackageVerificationCode, ExternalPackageRef, ExternalPackageRefCategory, \
    PackagePurpose
from tests.fixtures import creation_info_fixture


@pytest.fixture
@mock.patch('src.jsonschema.checksum_converter.ChecksumConverter', autospec=True)
@mock.patch('src.jsonschema.annotation_converter.AnnotationConverter', autospec=True)
@mock.patch('src.jsonschema.package_verification_code_converter.PackageVerificationCodeConverter', autospec=True)
@mock.patch('src.jsonschema.external_package_ref_converter.ExternalPackageRefConverter', autospec=True)
def converter(checksum_converter_mock: MagicMock, annotation_converter_mock: MagicMock,
              verification_code_converter_mock: MagicMock,
              package_ref_converter_mock: MagicMock) -> PackageConverter:
    converter = PackageConverter()
    converter.checksum_converter = checksum_converter_mock()
    converter.annotation_converter = annotation_converter_mock()
    converter.package_verification_code_converter = verification_code_converter_mock()
    converter.external_package_ref_converter = package_ref_converter_mock()
    return converter


@pytest.mark.parametrize("external_package_ref_property,expected",
                         [(PackageProperty.SPDX_ID, "SPDXID"),
                          (PackageProperty.ANNOTATIONS, "annotations"),
                          (PackageProperty.ATTRIBUTION_TEXTS, "attributionTexts"),
                          (PackageProperty.BUILT_DATE, "builtDate"),
                          (PackageProperty.CHECKSUMS, "checksums"),
                          (PackageProperty.COMMENT, "comment"),
                          (PackageProperty.COPYRIGHT_TEXT, "copyrightText"),
                          (PackageProperty.DESCRIPTION, "description"),
                          (PackageProperty.DOWNLOAD_LOCATION, "downloadLocation"),
                          (PackageProperty.EXTERNAL_REFS, "externalRefs"),
                          (PackageProperty.FILES_ANALYZED, "filesAnalyzed"),
                          (PackageProperty.HAS_FILES, "hasFiles"),
                          (PackageProperty.HOMEPAGE, "homepage"),
                          (PackageProperty.LICENSE_COMMENTS, "licenseComments"),
                          (PackageProperty.LICENSE_CONCLUDED, "licenseConcluded"),
                          (PackageProperty.LICENSE_DECLARED, "licenseDeclared"),
                          (PackageProperty.LICENSE_INFO_FROM_FILES, "licenseInfoFromFiles"),
                          (PackageProperty.NAME, "name"),
                          (PackageProperty.ORIGINATOR, "originator"),
                          (PackageProperty.PACKAGE_FILE_NAME, "packageFileName"),
                          (PackageProperty.PACKAGE_VERIFICATION_CODE, "packageVerificationCode"),
                          (PackageProperty.PRIMARY_PACKAGE_PURPOSE, "primaryPackagePurpose"),
                          (PackageProperty.RELEASE_DATE, "releaseDate"),
                          (PackageProperty.SOURCE_INFO, "sourceInfo"),
                          (PackageProperty.SUMMARY, "summary"),
                          (PackageProperty.SUPPLIER, "supplier"),
                          (PackageProperty.VALID_UNTIL_DATE, "validUntilDate"),
                          (PackageProperty.VERSION_INFO, "versionInfo")])
def test_json_property_names(converter: PackageConverter,
                             external_package_ref_property: PackageProperty, expected: str):
    assert converter.json_property_name(external_package_ref_property) == expected


def test_json_type(converter: PackageConverter):
    assert converter.get_json_type() == PackageProperty


def test_data_model_type(converter: PackageConverter):
    assert converter.get_data_model_type() == Package


def test_successful_conversion(converter: PackageConverter):
    converter.checksum_converter.convert.return_value = "mock_converted_checksum"
    converter.annotation_converter.convert.return_value = "mock_converted_annotation"
    converter.package_verification_code_converter.convert.return_value = "mock_converted_verification_code"
    converter.external_package_ref_converter.convert.return_value = "mock_package_ref"
    package = Package(spdx_id="packageId", name="name", download_location="downloadLocation", version="version",
                      file_name="fileName", supplier=Actor(ActorType.PERSON, "supplierName"),
                      originator=Actor(ActorType.PERSON, "originatorName"), files_analyzed=True,
                      verification_code=PackageVerificationCode("value"),
                      checksums=[Checksum(ChecksumAlgorithm.SHA1, "sha1"),
                                 Checksum(ChecksumAlgorithm.BLAKE2B_256, "blake")], homepage="homepage",
                      source_info="sourceInfo", license_concluded=LicenseExpression("licenseExpression1"),
                      license_info_from_files=[LicenseExpression("licenseExpression2"),
                                               LicenseExpression("licenseExpression3")],
                      license_declared=LicenseExpression("licenseExpression4"), license_comment="licenseComment",
                      copyright_text="copyrightText", summary="summary", description="description", comment="comment",
                      external_references=[
                          ExternalPackageRef(ExternalPackageRefCategory.PACKAGE_MANAGER, "referenceType",
                                             "referenceLocator")],
                      attribution_texts=["attributionText1", "attributionText2"],
                      primary_package_purpose=PackagePurpose.APPLICATION, release_date=datetime(2022, 12, 1),
                      built_date=datetime(2022, 12, 2), valid_until_date=datetime(2022, 12, 3))

    annotation = Annotation(package.spdx_id, AnnotationType.REVIEW, Actor(ActorType.TOOL, "toolName"),
                            datetime(2022, 12, 5),
                            "review comment")
    document = Document(creation_info_fixture(), packages=[package], annotations=[annotation])

    converted_dict = converter.convert(package, document)

    assert converted_dict[converter.json_property_name(PackageProperty.SPDX_ID)] == "packageId"
    assert converted_dict[converter.json_property_name(PackageProperty.ANNOTATIONS)] == ["mock_converted_annotation"]
    assert converted_dict[converter.json_property_name(PackageProperty.ATTRIBUTION_TEXTS)] == ["attributionText1",
                                                                                               "attributionText2"]
    assert converted_dict[converter.json_property_name(PackageProperty.NAME)] == "name"
    assert converted_dict[converter.json_property_name(PackageProperty.DOWNLOAD_LOCATION)] == "downloadLocation"
    assert converted_dict[converter.json_property_name(PackageProperty.VERSION_INFO)] == "version"
    assert converted_dict[converter.json_property_name(PackageProperty.PACKAGE_FILE_NAME)] == "fileName"
    assert converted_dict[converter.json_property_name(PackageProperty.SUPPLIER)] == "Person: supplierName"
    assert converted_dict[converter.json_property_name(PackageProperty.ORIGINATOR)] == "Person: originatorName"
    assert converted_dict[converter.json_property_name(PackageProperty.FILES_ANALYZED)]
    assert converted_dict[converter.json_property_name(
        PackageProperty.PACKAGE_VERIFICATION_CODE)] == "mock_converted_verification_code"
    assert converted_dict[converter.json_property_name(PackageProperty.CHECKSUMS)] == ["mock_converted_checksum",
                                                                                       "mock_converted_checksum"]
    assert converted_dict[converter.json_property_name(PackageProperty.HOMEPAGE)] == "homepage"
    assert converted_dict[converter.json_property_name(PackageProperty.SOURCE_INFO)] == "sourceInfo"
    assert converted_dict[converter.json_property_name(PackageProperty.LICENSE_CONCLUDED)] == "licenseExpression1"
    assert converted_dict[converter.json_property_name(PackageProperty.LICENSE_INFO_FROM_FILES)] == [
        "licenseExpression2", "licenseExpression3"]
    assert converted_dict[converter.json_property_name(PackageProperty.LICENSE_DECLARED)] == "licenseExpression4"
    assert converted_dict[converter.json_property_name(PackageProperty.LICENSE_COMMENTS)] == "licenseComment"
    assert converted_dict[converter.json_property_name(PackageProperty.COPYRIGHT_TEXT)] == "copyrightText"
    assert converted_dict[converter.json_property_name(PackageProperty.SUMMARY)] == "summary"
    assert converted_dict[converter.json_property_name(PackageProperty.DESCRIPTION)] == "description"
    assert converted_dict[converter.json_property_name(PackageProperty.COMMENT)] == "comment"
    assert converted_dict[converter.json_property_name(PackageProperty.EXTERNAL_REFS)] == ["mock_package_ref"]
    assert converted_dict[converter.json_property_name(PackageProperty.PRIMARY_PACKAGE_PURPOSE)] == "APPLICATION"
    assert converted_dict[converter.json_property_name(PackageProperty.RELEASE_DATE)] == "2022-12-01T00:00:00Z"
    assert converted_dict[converter.json_property_name(PackageProperty.BUILT_DATE)] == "2022-12-02T00:00:00Z"
    assert converted_dict[converter.json_property_name(PackageProperty.VALID_UNTIL_DATE)] == "2022-12-03T00:00:00Z"


def test_null_values(converter: PackageConverter):
    package = Package(spdx_id="packageId", name="name", download_location="downloadLocation")

    document = Document(creation_info_fixture(), packages=[package])

    converted_dict = converter.convert(package, document)

    assert converter.json_property_name(PackageProperty.VERSION_INFO) not in converted_dict
    assert converter.json_property_name(PackageProperty.PACKAGE_FILE_NAME) not in converted_dict
    assert converter.json_property_name(PackageProperty.SUPPLIER) not in converted_dict
    assert converter.json_property_name(PackageProperty.ORIGINATOR) not in converted_dict
    assert converter.json_property_name(PackageProperty.PACKAGE_VERIFICATION_CODE) not in converted_dict
    assert converter.json_property_name(PackageProperty.HOMEPAGE) not in converted_dict
    assert converter.json_property_name(PackageProperty.SOURCE_INFO) not in converted_dict
    assert converter.json_property_name(PackageProperty.LICENSE_CONCLUDED) not in converted_dict
    assert converter.json_property_name(PackageProperty.LICENSE_DECLARED) not in converted_dict
    assert converter.json_property_name(PackageProperty.LICENSE_COMMENTS) not in converted_dict
    assert converter.json_property_name(PackageProperty.COPYRIGHT_TEXT) not in converted_dict
    assert converter.json_property_name(PackageProperty.SUMMARY) not in converted_dict
    assert converter.json_property_name(PackageProperty.DESCRIPTION) not in converted_dict
    assert converter.json_property_name(PackageProperty.COMMENT) not in converted_dict
    assert converter.json_property_name(PackageProperty.PRIMARY_PACKAGE_PURPOSE) not in converted_dict
    assert converter.json_property_name(PackageProperty.BUILT_DATE) not in converted_dict
    assert converter.json_property_name(PackageProperty.RELEASE_DATE) not in converted_dict
    assert converter.json_property_name(PackageProperty.VALID_UNTIL_DATE) not in converted_dict
