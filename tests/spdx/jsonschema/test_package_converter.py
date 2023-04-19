# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime
from typing import Union
from unittest import mock
from unittest.mock import MagicMock, NonCallableMagicMock

import pytest
from license_expression import Licensing

from spdx_tools.spdx.jsonschema.annotation_converter import AnnotationConverter
from spdx_tools.spdx.jsonschema.package_converter import PackageConverter
from spdx_tools.spdx.jsonschema.package_properties import PackageProperty
from spdx_tools.spdx.model import (
    Actor,
    ActorType,
    Annotation,
    AnnotationType,
    Checksum,
    ChecksumAlgorithm,
    Document,
    Package,
    PackagePurpose,
    PackageVerificationCode,
    SpdxNoAssertion,
    SpdxNone,
)
from spdx_tools.spdx.model.spdx_no_assertion import SPDX_NO_ASSERTION_STRING
from spdx_tools.spdx.model.spdx_none import SPDX_NONE_STRING
from tests.spdx.fixtures import (
    annotation_fixture,
    creation_info_fixture,
    document_fixture,
    external_package_ref_fixture,
    package_fixture,
)
from tests.spdx.mock_utils import assert_mock_method_called_with_arguments


@pytest.fixture
@mock.patch("spdx_tools.spdx.jsonschema.checksum_converter.ChecksumConverter", autospec=True)
@mock.patch("spdx_tools.spdx.jsonschema.annotation_converter.AnnotationConverter", autospec=True)
@mock.patch(
    "spdx_tools.spdx.jsonschema.package_verification_code_converter.PackageVerificationCodeConverter", autospec=True
)
@mock.patch("spdx_tools.spdx.jsonschema.external_package_ref_converter.ExternalPackageRefConverter", autospec=True)
def converter(
    package_ref_converter_mock: MagicMock,
    verification_code_converter_mock: MagicMock,
    annotation_converter_mock: MagicMock,
    checksum_converter_mock: MagicMock,
) -> PackageConverter:
    converter = PackageConverter()
    converter.checksum_converter = checksum_converter_mock()
    converter.annotation_converter = annotation_converter_mock()
    converter.package_verification_code_converter = verification_code_converter_mock()
    converter.external_package_ref_converter = package_ref_converter_mock()
    return converter


@pytest.mark.parametrize(
    "external_package_ref_property,expected",
    [
        (PackageProperty.SPDX_ID, "SPDXID"),
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
        (PackageProperty.VERSION_INFO, "versionInfo"),
    ],
)
def test_json_property_names(
    converter: PackageConverter, external_package_ref_property: PackageProperty, expected: str
):
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
    package = Package(
        spdx_id="packageId",
        name="name",
        download_location="downloadLocation",
        version="version",
        file_name="fileName",
        supplier=Actor(ActorType.PERSON, "supplierName"),
        originator=Actor(ActorType.PERSON, "originatorName"),
        files_analyzed=True,
        verification_code=PackageVerificationCode("value"),
        checksums=[Checksum(ChecksumAlgorithm.SHA1, "sha1"), Checksum(ChecksumAlgorithm.BLAKE2B_256, "blake")],
        homepage="homepage",
        source_info="sourceInfo",
        license_concluded=Licensing().parse("MIT and GPL-2.0"),
        license_info_from_files=[Licensing().parse("MIT"), Licensing().parse("GPL-2.0")],
        license_declared=Licensing().parse("MIT or GPL-2.0 "),
        license_comment="licenseComment",
        copyright_text="copyrightText",
        summary="summary",
        description="description",
        comment="comment",
        external_references=[external_package_ref_fixture()],
        attribution_texts=["attributionText1", "attributionText2"],
        primary_package_purpose=PackagePurpose.APPLICATION,
        release_date=datetime(2022, 12, 1),
        built_date=datetime(2022, 12, 2),
        valid_until_date=datetime(2022, 12, 3),
    )

    annotation = Annotation(
        package.spdx_id,
        AnnotationType.REVIEW,
        Actor(ActorType.TOOL, "toolName"),
        datetime(2022, 12, 5),
        "review comment",
    )
    document = Document(creation_info_fixture(), packages=[package], annotations=[annotation])

    converted_dict = converter.convert(package, document)

    assert converted_dict == {
        converter.json_property_name(PackageProperty.SPDX_ID): "packageId",
        converter.json_property_name(PackageProperty.ANNOTATIONS): ["mock_converted_annotation"],
        converter.json_property_name(PackageProperty.ATTRIBUTION_TEXTS): ["attributionText1", "attributionText2"],
        converter.json_property_name(PackageProperty.NAME): "name",
        converter.json_property_name(PackageProperty.DOWNLOAD_LOCATION): "downloadLocation",
        converter.json_property_name(PackageProperty.VERSION_INFO): "version",
        converter.json_property_name(PackageProperty.PACKAGE_FILE_NAME): "fileName",
        converter.json_property_name(PackageProperty.SUPPLIER): "Person: supplierName",
        converter.json_property_name(PackageProperty.ORIGINATOR): "Person: originatorName",
        converter.json_property_name(PackageProperty.FILES_ANALYZED): True,
        converter.json_property_name(PackageProperty.PACKAGE_VERIFICATION_CODE): "mock_converted_verification_code",
        converter.json_property_name(PackageProperty.CHECKSUMS): [
            "mock_converted_checksum",
            "mock_converted_checksum",
        ],
        converter.json_property_name(PackageProperty.HOMEPAGE): "homepage",
        converter.json_property_name(PackageProperty.SOURCE_INFO): "sourceInfo",
        converter.json_property_name(PackageProperty.LICENSE_CONCLUDED): "MIT AND GPL-2.0",
        converter.json_property_name(PackageProperty.LICENSE_INFO_FROM_FILES): ["MIT", "GPL-2.0"],
        converter.json_property_name(PackageProperty.LICENSE_DECLARED): "MIT OR GPL-2.0",
        converter.json_property_name(PackageProperty.LICENSE_COMMENTS): "licenseComment",
        converter.json_property_name(PackageProperty.COPYRIGHT_TEXT): "copyrightText",
        converter.json_property_name(PackageProperty.SUMMARY): "summary",
        converter.json_property_name(PackageProperty.DESCRIPTION): "description",
        converter.json_property_name(PackageProperty.COMMENT): "comment",
        converter.json_property_name(PackageProperty.EXTERNAL_REFS): ["mock_package_ref"],
        converter.json_property_name(PackageProperty.PRIMARY_PACKAGE_PURPOSE): "APPLICATION",
        converter.json_property_name(PackageProperty.RELEASE_DATE): "2022-12-01T00:00:00Z",
        converter.json_property_name(PackageProperty.BUILT_DATE): "2022-12-02T00:00:00Z",
        converter.json_property_name(PackageProperty.VALID_UNTIL_DATE): "2022-12-03T00:00:00Z",
    }


def test_null_values(converter: PackageConverter):
    package = package_fixture(
        built_date=None,
        release_date=None,
        valid_until_date=None,
        homepage=None,
        license_concluded=None,
        license_declared=None,
        originator=None,
        verification_code=None,
        primary_package_purpose=None,
        supplier=None,
        version=None,
        file_name=None,
        source_info=None,
        license_comment=None,
        copyright_text=None,
        summary=None,
        description=None,
        comment=None,
        attribution_texts=[],
        checksums=[],
        external_references=[],
        license_info_from_files=[],
    )

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
    assert converter.json_property_name(PackageProperty.ANNOTATIONS) not in converted_dict
    assert converter.json_property_name(PackageProperty.ATTRIBUTION_TEXTS) not in converted_dict
    assert converter.json_property_name(PackageProperty.CHECKSUMS) not in converted_dict
    assert converter.json_property_name(PackageProperty.EXTERNAL_REFS) not in converted_dict
    assert converter.json_property_name(PackageProperty.LICENSE_INFO_FROM_FILES) not in converted_dict


def test_spdx_no_assertion(converter: PackageConverter):
    package = package_fixture(
        download_location=SpdxNoAssertion(),
        supplier=SpdxNoAssertion(),
        originator=SpdxNoAssertion(),
        homepage=SpdxNoAssertion(),
        license_concluded=SpdxNoAssertion(),
        license_info_from_files=[SpdxNoAssertion()],
        license_declared=SpdxNoAssertion(),
        copyright_text=SpdxNoAssertion(),
    )

    document = Document(creation_info_fixture(), packages=[package])

    converted_dict = converter.convert(package, document)

    assert converted_dict[converter.json_property_name(PackageProperty.DOWNLOAD_LOCATION)] == SPDX_NO_ASSERTION_STRING
    assert converted_dict[converter.json_property_name(PackageProperty.SUPPLIER)] == SPDX_NO_ASSERTION_STRING
    assert converted_dict[converter.json_property_name(PackageProperty.ORIGINATOR)] == SPDX_NO_ASSERTION_STRING
    assert converted_dict[converter.json_property_name(PackageProperty.HOMEPAGE)] == SPDX_NO_ASSERTION_STRING
    assert converted_dict[converter.json_property_name(PackageProperty.LICENSE_CONCLUDED)] == SPDX_NO_ASSERTION_STRING
    assert converted_dict[converter.json_property_name(PackageProperty.LICENSE_INFO_FROM_FILES)] == [
        SPDX_NO_ASSERTION_STRING
    ]
    assert converted_dict[converter.json_property_name(PackageProperty.LICENSE_DECLARED)] == SPDX_NO_ASSERTION_STRING
    assert converted_dict[converter.json_property_name(PackageProperty.COPYRIGHT_TEXT)] == SPDX_NO_ASSERTION_STRING


def test_spdx_none(converter: PackageConverter):
    package = package_fixture(
        download_location=SpdxNone(),
        homepage=SpdxNone(),
        license_concluded=SpdxNone(),
        license_info_from_files=[SpdxNone()],
        license_declared=SpdxNone(),
        copyright_text=SpdxNone(),
    )

    document = Document(creation_info_fixture(), packages=[package])

    converted_dict = converter.convert(package, document)

    assert converted_dict[converter.json_property_name(PackageProperty.DOWNLOAD_LOCATION)] == SPDX_NONE_STRING
    assert converted_dict[converter.json_property_name(PackageProperty.HOMEPAGE)] == SPDX_NONE_STRING
    assert converted_dict[converter.json_property_name(PackageProperty.LICENSE_CONCLUDED)] == SPDX_NONE_STRING
    assert converted_dict[converter.json_property_name(PackageProperty.LICENSE_INFO_FROM_FILES)] == [SPDX_NONE_STRING]
    assert converted_dict[converter.json_property_name(PackageProperty.LICENSE_DECLARED)] == SPDX_NONE_STRING
    assert converted_dict[converter.json_property_name(PackageProperty.COPYRIGHT_TEXT)] == SPDX_NONE_STRING


def test_package_annotations(converter: PackageConverter):
    package = package_fixture(spdx_id="packageId")
    document = document_fixture(packages=[package])
    first_package_annotation = annotation_fixture(spdx_id=package.spdx_id)
    second_package_annotation = annotation_fixture(spdx_id=package.spdx_id)
    document_annotation = annotation_fixture(spdx_id=document.creation_info.spdx_id)
    file_annotation = annotation_fixture(spdx_id=document.files[0].spdx_id)
    snippet_annotation = annotation_fixture(spdx_id=document.snippets[0].spdx_id)
    other_annotation = annotation_fixture(spdx_id="otherId")
    annotations = [
        first_package_annotation,
        second_package_annotation,
        document_annotation,
        file_annotation,
        snippet_annotation,
        other_annotation,
    ]
    document.annotations = annotations

    # Weird type hint to make warnings about unresolved references from the mock class disappear
    annotation_converter: Union[AnnotationConverter, NonCallableMagicMock] = converter.annotation_converter
    annotation_converter.convert.return_value = "mock_converted_annotation"

    converted_dict = converter.convert(package, document)

    assert_mock_method_called_with_arguments(
        annotation_converter, "convert", first_package_annotation, second_package_annotation
    )
    converted_file_annotations = converted_dict.get(converter.json_property_name(PackageProperty.ANNOTATIONS))
    assert converted_file_annotations == ["mock_converted_annotation", "mock_converted_annotation"]
