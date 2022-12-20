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

from src.jsonschema.document_converter import DocumentConverter
from src.jsonschema.document_properties import DocumentProperty
from src.model.actor import Actor, ActorType
from src.model.annotation import Annotation, AnnotationType
from src.model.checksum import Checksum, ChecksumAlgorithm
from src.model.document import Document, CreationInfo
from src.model.external_document_ref import ExternalDocumentRef
from src.model.extracted_licensing_info import ExtractedLicensingInfo
from src.model.file import File
from src.model.package import Package
from src.model.relationship import Relationship, RelationshipType
from src.model.snippet import Snippet
from src.model.spdx_none import SpdxNone


@pytest.fixture
@mock.patch('src.jsonschema.creation_info_converter.CreationInfoConverter', autospec=True)
@mock.patch('src.jsonschema.external_document_ref_converter.ExternalDocumentRefConverter', autospec=True)
@mock.patch('src.jsonschema.package_converter.PackageConverter', autospec=True)
@mock.patch('src.jsonschema.annotation_converter.AnnotationConverter', autospec=True)
@mock.patch('src.jsonschema.extracted_licensing_info_converter.ExtractedLicensingInfoConverter', autospec=True)
@mock.patch('src.jsonschema.file_converter.FileConverter', autospec=True)
@mock.patch('src.jsonschema.snippet_converter.SnippetConverter', autospec=True)
@mock.patch('src.jsonschema.relationship_converter.RelationshipConverter', autospec=True)
def converter(external_ref_converter_mock: MagicMock, creation_info_converter_mock: MagicMock,
              package_converter_mock: MagicMock, annotation_converter_mock: MagicMock,
              extracted_licensing_info_converter_mock: MagicMock, file_converter_mock: MagicMock,
              snippet_converter_mock: MagicMock, relationship_converter_mock: MagicMock) -> DocumentConverter:
    converter = DocumentConverter()
    converter.creation_info_converter = creation_info_converter_mock()
    converter.external_document_ref_converter = external_ref_converter_mock()
    converter.package_converter = package_converter_mock()
    converter.annotation_converter = annotation_converter_mock()
    converter.extracted_licensing_info_converter = extracted_licensing_info_converter_mock()
    converter.file_converter = file_converter_mock()
    converter.snippet_converter = snippet_converter_mock()
    converter.relationship_converter = relationship_converter_mock()
    return converter


@pytest.mark.parametrize("document_property,expected",
                         [(DocumentProperty.SPDX_VERSION, "spdxVersion"), (DocumentProperty.SPDX_ID, "SPDXID"),
                          (DocumentProperty.NAME, "name"), (DocumentProperty.DOCUMENT_NAMESPACE, "documentNamespace"),
                          (DocumentProperty.DATA_LICENSE, "dataLicense"),
                          (DocumentProperty.EXTERNAL_DOCUMENT_REFS, "externalDocumentRefs"),
                          (DocumentProperty.COMMENT, "comment"), (DocumentProperty.CREATION_INFO, "creationInfo"),
                          (DocumentProperty.PACKAGES, "packages"), (DocumentProperty.FILES, "files"),
                          (DocumentProperty.SNIPPETS, "snippets"), (DocumentProperty.ANNOTATIONS, "annotations"),
                          (DocumentProperty.RELATIONSHIPS, "relationships"),
                          (DocumentProperty.HAS_EXTRACTED_LICENSING_INFO, "hasExtractedLicensingInfo")])
def test_json_property_names(converter: DocumentConverter, document_property: DocumentProperty,
                             expected: str):
    assert converter.json_property_name(document_property) == expected


def test_successful_conversion(converter: DocumentConverter):
    creation_info = CreationInfo("spdxVersion", "spdxId", "name", "namespace", [], datetime.today(),
                                 document_comment="comment", data_license="dataLicense", external_document_refs=[
            ExternalDocumentRef("docRefId", "externalDocumentUri", Checksum(ChecksumAlgorithm.SHA1, "sha1"))])
    package = Package("packageID", "packageName", SpdxNone())
    file = File("fileName", "fileId", [])
    snippet = Snippet("snippetId", "snippetFileId", (1, 2))
    document = Document(creation_info, annotations=[
        Annotation("annotationId", AnnotationType.REVIEW, Actor(ActorType.PERSON, "reviewerName"),
                   datetime(2022, 12, 1), "reviewComment")],
                        extracted_licensing_info=[ExtractedLicensingInfo("licenseId", "licenseText")], relationships=[
            Relationship(creation_info.spdx_id, RelationshipType.DESCRIBES, "describedElementId"),
            Relationship("relationshipOriginId", RelationshipType.AMENDS, "relationShipTargetId")], packages=[package],
                        files=[file], snippets=[snippet])
    converter.external_document_ref_converter.convert.return_value = "mock_converted_external_ref"
    converter.creation_info_converter.convert.return_value = "mock_converted_creation_info"
    converter.package_converter.convert.return_value = "mock_converted_package"
    converter.annotation_converter.convert.return_value = "mock_converted_annotation"
    converter.extracted_licensing_info_converter.convert.return_value = "mock_converted_extracted_licensing_info"
    converter.package_converter.convert.return_value = "mock_converted_package"
    converter.file_converter.convert.return_value = "mock_converted_file"
    converter.snippet_converter.convert.return_value = "mock_converted_snippet"
    converter.relationship_converter.convert.return_value = "mock_converted_relationship"

    converted_dict = converter.convert(document)

    assert converted_dict[converter.json_property_name(DocumentProperty.SPDX_ID)] == "spdxId"
    assert converted_dict[converter.json_property_name(DocumentProperty.ANNOTATIONS)] == ["mock_converted_annotation"]
    assert converted_dict[converter.json_property_name(DocumentProperty.COMMENT)] == "comment"
    assert converted_dict[
               converter.json_property_name(DocumentProperty.CREATION_INFO)] == "mock_converted_creation_info"
    assert converted_dict[converter.json_property_name(DocumentProperty.DATA_LICENSE)] == "dataLicense"
    assert converted_dict[
               converter.json_property_name(
                   DocumentProperty.EXTERNAL_DOCUMENT_REFS)] == ["mock_converted_external_ref"]
    assert converted_dict[converter.json_property_name(DocumentProperty.HAS_EXTRACTED_LICENSING_INFO)] == [
        "mock_converted_extracted_licensing_info"]
    assert converted_dict[converter.json_property_name(DocumentProperty.NAME)] == "name"
    assert converted_dict[converter.json_property_name(DocumentProperty.SPDX_VERSION)] == "spdxVersion"
    assert converted_dict[converter.json_property_name(DocumentProperty.DOCUMENT_NAMESPACE)] == "namespace"
    assert converted_dict[converter.json_property_name(DocumentProperty.DOCUMENT_DESCRIBES)] == ["describedElementId"]
    assert converted_dict[converter.json_property_name(DocumentProperty.PACKAGES)] == ["mock_converted_package"]
    assert converted_dict[converter.json_property_name(DocumentProperty.FILES)] == ["mock_converted_file"]
    assert converted_dict[converter.json_property_name(DocumentProperty.SNIPPETS)] == ["mock_converted_snippet"]
    assert converted_dict[converter.json_property_name(DocumentProperty.RELATIONSHIPS)] == [
        "mock_converted_relationship"]


def test_json_type(converter: DocumentConverter):
    assert converter.get_json_type() == DocumentProperty


def test_data_model_type(converter: DocumentConverter):
    assert converter.get_data_model_type() == Document
