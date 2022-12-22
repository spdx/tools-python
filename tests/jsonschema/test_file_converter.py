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
from typing import Union
from unittest import mock
from unittest.mock import MagicMock, NonCallableMagicMock

import pytest

from src.jsonschema.annotation_converter import AnnotationConverter
from src.jsonschema.file_converter import FileConverter
from src.jsonschema.file_properties import FileProperty
from src.model.actor import Actor, ActorType
from src.model.annotation import Annotation, AnnotationType
from src.model.checksum import Checksum, ChecksumAlgorithm
from src.model.document import Document
from src.model.file import File, FileType
from src.model.license_expression import LicenseExpression
from src.model.spdx_no_assertion import SpdxNoAssertion, SPDX_NO_ASSERTION_STRING
from src.model.spdx_none import SpdxNone, SPDX_NONE_STRING
from tests.fixtures import creation_info_fixture, file_fixture, annotation_fixture, document_fixture
from tests.mock_utils import assert_mock_method_called_with_arguments


@pytest.fixture
@mock.patch('src.jsonschema.checksum_converter.ChecksumConverter', autospec=True)
@mock.patch('src.jsonschema.annotation_converter.AnnotationConverter', autospec=True)
def converter(annotation_converter_mock: MagicMock, checksum_converter_mock: MagicMock) -> FileConverter:
    converter = FileConverter()
    converter.checksum_converter = checksum_converter_mock()
    converter.annotation_converter = annotation_converter_mock()
    return converter


@pytest.mark.parametrize("file_property,expected",
                         [(FileProperty.SPDX_ID, "SPDXID"),
                          (FileProperty.ANNOTATIONS, "annotations"),
                          (FileProperty.ARTIFACT_OFS, "artifactOfs"),
                          (FileProperty.ATTRIBUTION_TEXTS, "attributionTexts"),
                          (FileProperty.CHECKSUMS, "checksums"),
                          (FileProperty.COMMENT, "comment"),
                          (FileProperty.COPYRIGHT_TEXT, "copyrightText"),
                          (FileProperty.FILE_CONTRIBUTORS, "fileContributors"),
                          (FileProperty.FILE_DEPENDENCIES, "fileDependencies"),
                          (FileProperty.FILE_NAME, "fileName"),
                          (FileProperty.FILE_TYPES, "fileTypes"),
                          (FileProperty.LICENSE_COMMENTS, "licenseComments"),
                          (FileProperty.LICENSE_CONCLUDED, "licenseConcluded"),
                          (FileProperty.LICENSE_INFO_IN_FILES, "licenseInfoInFiles"),
                          (FileProperty.NOTICE_TEXT, "noticeText")])
def test_json_property_names(converter: FileConverter, file_property: FileProperty, expected: str):
    assert converter.json_property_name(file_property) == expected


def test_json_type(converter: FileConverter):
    assert converter.get_json_type() == FileProperty


def test_data_model_type(converter: FileConverter):
    assert converter.get_data_model_type() == File


def test_successful_conversion(converter: FileConverter):
    converter.checksum_converter.convert.return_value = "mock_converted_checksum"
    converter.annotation_converter.convert.return_value = "mock_converted_annotation"
    file = File(name="name", spdx_id="spdxId",
                checksums=[Checksum(ChecksumAlgorithm.SHA224, "sha224"), Checksum(ChecksumAlgorithm.MD2, "md2")],
                file_type=[FileType.SPDX, FileType.OTHER], concluded_license=LicenseExpression("licenseExpression1"),
                license_info_in_file=[LicenseExpression("licenseExpression2"), LicenseExpression("licenseExpression3")],
                license_comment="licenseComment", copyright_text="copyrightText", comment="comment", notice="notice",
                contributors=["contributor1", "contributor2"],
                attribution_texts=["attributionText1", "attributionText2"])

    annotations = [Annotation(file.spdx_id, AnnotationType.REVIEW, Actor(ActorType.PERSON, "annotatorName"),
                              datetime(2022, 12, 5), "review comment")]
    document = Document(creation_info_fixture(), files=[file], annotations=annotations)

    converted_dict = converter.convert(file, document)

    assert converted_dict == {
        converter.json_property_name(FileProperty.SPDX_ID): "spdxId",
        converter.json_property_name(FileProperty.ANNOTATIONS): ["mock_converted_annotation"],
        converter.json_property_name(FileProperty.ATTRIBUTION_TEXTS): ["attributionText1", "attributionText2"],
        converter.json_property_name(FileProperty.CHECKSUMS): ["mock_converted_checksum", "mock_converted_checksum"],
        converter.json_property_name(FileProperty.COMMENT): "comment",
        converter.json_property_name(FileProperty.COPYRIGHT_TEXT): "copyrightText",
        converter.json_property_name(FileProperty.FILE_CONTRIBUTORS): ["contributor1", "contributor2"],
        converter.json_property_name(FileProperty.FILE_NAME): "name",
        converter.json_property_name(FileProperty.FILE_TYPES): ["SPDX", "OTHER"],
        converter.json_property_name(FileProperty.LICENSE_COMMENTS): "licenseComment",
        converter.json_property_name(FileProperty.LICENSE_CONCLUDED): "licenseExpression1",
        converter.json_property_name(FileProperty.LICENSE_INFO_IN_FILES): ["licenseExpression2", "licenseExpression3"],
        converter.json_property_name(FileProperty.NOTICE_TEXT): "notice"
    }


def test_null_values(converter: FileConverter):
    file = file_fixture(copyright_text=None, concluded_license=None, license_comment=None, comment=None, notice=None,
                        attribution_texts=[], checksums=[], contributors=[], file_type=[], license_info_in_file=[])
    document = Document(creation_info_fixture(), files=[file])

    converted_dict = converter.convert(file, document)

    assert converter.json_property_name(FileProperty.COPYRIGHT_TEXT) not in converted_dict
    assert converter.json_property_name(FileProperty.LICENSE_CONCLUDED) not in converted_dict
    assert converter.json_property_name(FileProperty.LICENSE_COMMENTS) not in converted_dict
    assert converter.json_property_name(FileProperty.COMMENT) not in converted_dict
    assert converter.json_property_name(FileProperty.NOTICE_TEXT) not in converted_dict
    assert converter.json_property_name(FileProperty.ANNOTATIONS) not in converted_dict
    assert converter.json_property_name(FileProperty.ATTRIBUTION_TEXTS) not in converted_dict
    assert converter.json_property_name(FileProperty.CHECKSUMS) not in converted_dict
    assert converter.json_property_name(FileProperty.FILE_CONTRIBUTORS) not in converted_dict
    assert converter.json_property_name(FileProperty.FILE_TYPES) not in converted_dict
    assert converter.json_property_name(FileProperty.LICENSE_INFO_IN_FILES) not in converted_dict


def test_spdx_no_assertion(converter: FileConverter):
    file = file_fixture(concluded_license=SpdxNoAssertion(), license_info_in_file=SpdxNoAssertion(),
                        copyright_text=SpdxNoAssertion())
    document = Document(creation_info_fixture(), files=[file])

    converted_dict = converter.convert(file, document)

    assert converted_dict[
               converter.json_property_name(FileProperty.COPYRIGHT_TEXT)] == SPDX_NO_ASSERTION_STRING
    assert converted_dict[converter.json_property_name(FileProperty.LICENSE_CONCLUDED)] == SPDX_NO_ASSERTION_STRING
    assert converted_dict[converter.json_property_name(FileProperty.LICENSE_INFO_IN_FILES)] == SPDX_NO_ASSERTION_STRING


def test_spdx_none(converter: FileConverter):
    file = file_fixture(concluded_license=SpdxNone(), license_info_in_file=SpdxNone(), copyright_text=SpdxNone())
    document = Document(creation_info_fixture(), files=[file])

    converted_dict = converter.convert(file, document)

    assert converted_dict[
               converter.json_property_name(FileProperty.COPYRIGHT_TEXT)] == SPDX_NONE_STRING
    assert converted_dict[converter.json_property_name(FileProperty.LICENSE_CONCLUDED)] == SPDX_NONE_STRING
    assert converted_dict[converter.json_property_name(FileProperty.LICENSE_INFO_IN_FILES)] == SPDX_NONE_STRING


def test_file_annotations(converter: FileConverter):
    file = file_fixture(spdx_id="fileId")
    document = document_fixture(files=[file])
    first_file_annotation = annotation_fixture(spdx_id=file.spdx_id)
    second_file_annotation = annotation_fixture(spdx_id=file.spdx_id)
    document_annotation = annotation_fixture(spdx_id=document.creation_info.spdx_id)
    package_annotation = annotation_fixture(spdx_id=document.packages[0].spdx_id)
    snippet_annotation = annotation_fixture(spdx_id=document.snippets[0].spdx_id)
    other_annotation = annotation_fixture(spdx_id="otherId")
    annotations = [first_file_annotation, second_file_annotation, document_annotation, package_annotation,
                   snippet_annotation, other_annotation]
    document.annotations = annotations

    # Weird type hint to make warnings about unresolved references from the mock class disappear
    annotation_converter: Union[AnnotationConverter, NonCallableMagicMock] = converter.annotation_converter
    annotation_converter.convert.return_value = "mock_converted_annotation"

    converted_dict = converter.convert(file, document)

    assert_mock_method_called_with_arguments(annotation_converter, "convert", first_file_annotation,
                                             second_file_annotation)
    converted_file_annotations = converted_dict.get(converter.json_property_name(FileProperty.ANNOTATIONS))
    assert converted_file_annotations == ["mock_converted_annotation", "mock_converted_annotation"]
