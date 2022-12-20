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

from src.jsonschema.file_converter import FileConverter
from src.jsonschema.file_properties import FileProperty
from src.model.actor import Actor, ActorType
from src.model.annotation import Annotation, AnnotationType
from src.model.checksum import Checksum, ChecksumAlgorithm
from src.model.document import CreationInfo, Document
from src.model.file import File, FileType
from src.model.license_expression import LicenseExpression


@pytest.fixture
@mock.patch('src.jsonschema.checksum_converter.ChecksumConverter', autospec=True)
@mock.patch('src.jsonschema.annotation_converter.AnnotationConverter', autospec=True)
def converter(checksum_converter_mock: MagicMock, annotation_converter_mock: MagicMock) -> FileConverter:
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

    creation_info = CreationInfo("spdxVersion", "documentID", "documentName", "documentNamespace", [],
                                 datetime(2022, 12, 4))

    annotations = [Annotation(file.spdx_id, AnnotationType.REVIEW, Actor(ActorType.PERSON, "annotatorName"),
                              datetime(2022, 12, 5), "review comment")]
    document = Document(creation_info, files=[file], annotations=annotations)

    converted_dict = converter.convert(file, document)

    assert converted_dict[converter.json_property_name(FileProperty.SPDX_ID)] == "spdxId"
    assert converted_dict[converter.json_property_name(FileProperty.ANNOTATIONS)] == ["mock_converted_annotation"]
    assert converted_dict[converter.json_property_name(FileProperty.ATTRIBUTION_TEXTS)] == ["attributionText1",
                                                                                            "attributionText2"]
    assert converted_dict[converter.json_property_name(FileProperty.CHECKSUMS)] == ["mock_converted_checksum",
                                                                                    "mock_converted_checksum"]
    assert converted_dict[converter.json_property_name(FileProperty.COMMENT)] == "comment"
    assert converted_dict[
               converter.json_property_name(FileProperty.COPYRIGHT_TEXT)] == "copyrightText"
    assert converted_dict[converter.json_property_name(FileProperty.FILE_CONTRIBUTORS)] == ["contributor1",
                                                                                            "contributor2"]
    assert converted_dict[converter.json_property_name(FileProperty.FILE_NAME)] == "name"
    assert converted_dict[converter.json_property_name(FileProperty.FILE_TYPES)] == ["SPDX", "OTHER"]
    assert converted_dict[converter.json_property_name(FileProperty.LICENSE_COMMENTS)] == "licenseComment"
    assert converted_dict[converter.json_property_name(FileProperty.LICENSE_CONCLUDED)] == "licenseExpression1"
    assert converted_dict[converter.json_property_name(FileProperty.LICENSE_INFO_IN_FILES)] == ["licenseExpression2",
                                                                                                "licenseExpression3"]
    assert converted_dict[converter.json_property_name(FileProperty.NOTICE_TEXT)] == "notice"


def test_null_values(converter: FileConverter):
    file = File(name="name", spdx_id="spdxId",
                checksums=[Checksum(ChecksumAlgorithm.SHA224, "sha224"), Checksum(ChecksumAlgorithm.MD2, "md2")])

    creation_info = CreationInfo("spdxVersion", "documentID", "documentName", "documentNamespace", [],
                                 datetime(2022, 12, 4))

    document = Document(creation_info, files=[file])

    converted_dict = converter.convert(file, document)

    assert converter.json_property_name(FileProperty.COPYRIGHT_TEXT) not in converted_dict
    assert converter.json_property_name(FileProperty.LICENSE_CONCLUDED) not in converted_dict
    assert converter.json_property_name(FileProperty.LICENSE_COMMENTS) not in converted_dict
    assert converter.json_property_name(FileProperty.COMMENT) not in converted_dict
    assert converter.json_property_name(FileProperty.NOTICE_TEXT) not in converted_dict
