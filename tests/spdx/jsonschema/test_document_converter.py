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
from datetime import datetime
from typing import Union
from unittest import mock
from unittest.mock import MagicMock, NonCallableMagicMock

import pytest

from spdx.jsonschema.annotation_converter import AnnotationConverter
from spdx.jsonschema.document_converter import DocumentConverter
from spdx.jsonschema.document_properties import DocumentProperty
from spdx.jsonschema.relationship_converter import RelationshipConverter
from spdx.model.actor import Actor, ActorType
from spdx.model.annotation import Annotation, AnnotationType
from spdx.model.document import Document
from spdx.model.extracted_licensing_info import ExtractedLicensingInfo
from spdx.model.relationship import Relationship, RelationshipType
from tests.spdx.fixtures import creation_info_fixture, file_fixture, package_fixture, external_document_ref_fixture, \
    snippet_fixture, annotation_fixture, document_fixture, relationship_fixture
from tests.spdx.mock_utils import assert_mock_method_called_with_arguments, assert_no_mock_methods_called


@pytest.fixture
@mock.patch('spdx.jsonschema.creation_info_converter.CreationInfoConverter', autospec=True)
@mock.patch('spdx.jsonschema.external_document_ref_converter.ExternalDocumentRefConverter', autospec=True)
@mock.patch('spdx.jsonschema.package_converter.PackageConverter', autospec=True)
@mock.patch('spdx.jsonschema.annotation_converter.AnnotationConverter', autospec=True)
@mock.patch('spdx.jsonschema.extracted_licensing_info_converter.ExtractedLicensingInfoConverter', autospec=True)
@mock.patch('spdx.jsonschema.file_converter.FileConverter', autospec=True)
@mock.patch('spdx.jsonschema.snippet_converter.SnippetConverter', autospec=True)
@mock.patch('spdx.jsonschema.relationship_converter.RelationshipConverter', autospec=True)
def converter(relationship_converter_mock: MagicMock, snippet_converter_mock: MagicMock, file_converter_mock: MagicMock,
              extracted_licensing_info_converter_mock: MagicMock, annotation_converter_mock: MagicMock,
              package_converter_mock: MagicMock, external_ref_converter_mock: MagicMock,
              creation_info_converter_mock: MagicMock) -> DocumentConverter:
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
                          (DocumentProperty.HAS_EXTRACTED_LICENSING_INFOS, "hasExtractedLicensingInfos")])
def test_json_property_names(converter: DocumentConverter, document_property: DocumentProperty,
                             expected: str):
    assert converter.json_property_name(document_property) == expected


def test_successful_conversion(converter: DocumentConverter):
    creation_info = creation_info_fixture(spdx_version="spdxVersion", spdx_id="spdxId", name="name",
                                          document_namespace="namespace", document_comment="comment", data_license="dataLicense",
                                          external_document_refs=[external_document_ref_fixture()])
    document = Document(creation_info, annotations=[
        Annotation("annotationId", AnnotationType.REVIEW, Actor(ActorType.PERSON, "reviewerName"),
                   datetime(2022, 12, 1), "reviewComment")],
                        extracted_licensing_info=[ExtractedLicensingInfo("licenseId", "licenseText")], relationships=[
            Relationship(creation_info.spdx_id, RelationshipType.DESCRIBES, "describedElementId"),
            Relationship("relationshipOriginId", RelationshipType.AMENDS, "relationShipTargetId")],
                        packages=[package_fixture()], files=[file_fixture()], snippets=[snippet_fixture()])
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

    assert converted_dict == {
        converter.json_property_name(DocumentProperty.SPDX_ID): "spdxId",
        converter.json_property_name(DocumentProperty.ANNOTATIONS): ["mock_converted_annotation"],
        converter.json_property_name(DocumentProperty.COMMENT): "comment",
        converter.json_property_name(DocumentProperty.CREATION_INFO): "mock_converted_creation_info",
        converter.json_property_name(DocumentProperty.DATA_LICENSE): "dataLicense",
        converter.json_property_name(DocumentProperty.EXTERNAL_DOCUMENT_REFS): ["mock_converted_external_ref"],
        converter.json_property_name(DocumentProperty.HAS_EXTRACTED_LICENSING_INFOS): [
            "mock_converted_extracted_licensing_info"],
        converter.json_property_name(DocumentProperty.NAME): "name",
        converter.json_property_name(DocumentProperty.SPDX_VERSION): "spdxVersion",
        converter.json_property_name(DocumentProperty.DOCUMENT_NAMESPACE): "namespace",
        converter.json_property_name(DocumentProperty.DOCUMENT_DESCRIBES): ["describedElementId"],
        converter.json_property_name(DocumentProperty.PACKAGES): ["mock_converted_package"],
        converter.json_property_name(DocumentProperty.FILES): ["mock_converted_file"],
        converter.json_property_name(DocumentProperty.SNIPPETS): ["mock_converted_snippet"],
        converter.json_property_name(DocumentProperty.RELATIONSHIPS): ["mock_converted_relationship"]
    }


def test_json_type(converter: DocumentConverter):
    assert converter.get_json_type() == DocumentProperty


def test_data_model_type(converter: DocumentConverter):
    assert converter.get_data_model_type() == Document


def test_null_values(converter: DocumentConverter):
    document = Document(creation_info_fixture(external_document_refs=[]))

    converted_dict = converter.convert(document)

    assert converter.json_property_name(DocumentProperty.ANNOTATIONS) not in converted_dict
    assert converter.json_property_name(DocumentProperty.EXTERNAL_DOCUMENT_REFS) not in converted_dict
    assert converter.json_property_name(DocumentProperty.HAS_EXTRACTED_LICENSING_INFOS) not in converted_dict
    assert converter.json_property_name(DocumentProperty.DOCUMENT_DESCRIBES) not in converted_dict
    assert converter.json_property_name(DocumentProperty.PACKAGES) not in converted_dict
    assert converter.json_property_name(DocumentProperty.FILES) not in converted_dict
    assert converter.json_property_name(DocumentProperty.SNIPPETS) not in converted_dict
    assert converter.json_property_name(DocumentProperty.RELATIONSHIPS) not in converted_dict


def test_document_annotations(converter: DocumentConverter):
    file = file_fixture(spdx_id="fileId")
    package = package_fixture(spdx_id="packageId")
    snippet = snippet_fixture(spdx_id="snippetId")
    document_id = "documentId"

    # There are 5 annotations: one each referencing the document, package, file and snippet, and one with an id
    # matching none of the Spdx elements. The writer is expected to add the package, file and snippet annotations to
    # those elements, so the document should receive the other two.
    document_annotation = annotation_fixture(spdx_id=document_id)
    other_annotation = annotation_fixture(spdx_id="otherId")
    annotations = [annotation_fixture(spdx_id=file.spdx_id), annotation_fixture(spdx_id=package.spdx_id),
                   annotation_fixture(spdx_id=snippet.spdx_id), document_annotation,
                   other_annotation]
    document = Document(creation_info_fixture(spdx_id=document_id), files=[file], packages=[package],
                        snippets=[snippet], annotations=annotations)

    # Weird type hint to make warnings about unresolved references from the mock class disappear
    annotation_converter: Union[AnnotationConverter, NonCallableMagicMock] = converter.annotation_converter
    annotation_converter.convert.return_value = "mock_converted_annotation"

    converted_dict = converter.convert(document)

    assert_mock_method_called_with_arguments(annotation_converter, "convert", document_annotation, other_annotation)
    converted_document_annotations = converted_dict.get(converter.json_property_name(DocumentProperty.ANNOTATIONS))
    assert converted_document_annotations == ["mock_converted_annotation", "mock_converted_annotation"]


def test_document_describes(converter: DocumentConverter):
    document = document_fixture()
    document_id = document.creation_info.spdx_id
    document_describes_relationship = relationship_fixture(spdx_element_id=document_id,
                                                           relationship_type=RelationshipType.DESCRIBES,
                                                           related_spdx_element_id="describesId")
    described_by_document_relationship = relationship_fixture(related_spdx_element_id=document_id,
                                                              relationship_type=RelationshipType.DESCRIBED_BY,
                                                              spdx_element_id="describedById")
    other_describes_relationship = relationship_fixture(spdx_element_id="DocumentRef-external",
                                                        relationship_type=RelationshipType.DESCRIBES)
    other_relationship = relationship_fixture(spdx_element_id=document_id, relationship_type=RelationshipType.CONTAINS)
    document.relationships = [document_describes_relationship, described_by_document_relationship,
                              other_describes_relationship, other_relationship]

    converted_dict = converter.convert(document)

    document_describes = converted_dict.get(converter.json_property_name(DocumentProperty.DOCUMENT_DESCRIBES))
    assert document_describes == [document_describes_relationship.related_spdx_element_id,
                                  described_by_document_relationship.spdx_element_id]


DOCUMENT_ID = "docConverterTestDocumentId"
PACKAGE_ID = "docConverterTestPackageId"
FILE_ID = "docConverterTestFileId"


@pytest.mark.parametrize("relationship,should_be_written",
                         [(relationship_fixture(DOCUMENT_ID, RelationshipType.DESCRIBES), True),
                          (relationship_fixture(DOCUMENT_ID, RelationshipType.DESCRIBES, comment=None), False),
                          (relationship_fixture(relationship_type=RelationshipType.DESCRIBED_BY,
                                                related_spdx_element_id=DOCUMENT_ID), True),
                          (relationship_fixture(relationship_type=RelationshipType.DESCRIBED_BY,
                                                related_spdx_element_id=DOCUMENT_ID, comment=None), False),
                          (relationship_fixture(DOCUMENT_ID, RelationshipType.AMENDS, comment=None), True),
                          (relationship_fixture(PACKAGE_ID, RelationshipType.CONTAINS, FILE_ID), True),
                          (relationship_fixture(PACKAGE_ID, RelationshipType.CONTAINS, FILE_ID, comment=None), False),
                          (relationship_fixture(FILE_ID, RelationshipType.CONTAINED_BY, PACKAGE_ID), True),
                          (relationship_fixture(FILE_ID, RelationshipType.CONTAINED_BY, PACKAGE_ID, comment=None),
                           False),
                          (relationship_fixture(PACKAGE_ID, RelationshipType.CONTAINS, comment=None), True),
                          (relationship_fixture(PACKAGE_ID, RelationshipType.COPY_OF, FILE_ID, comment=None), True)])
def test_document_relationships(converter: DocumentConverter, relationship: Relationship, should_be_written: bool):
    package = package_fixture(spdx_id=PACKAGE_ID)
    file = file_fixture(spdx_id=FILE_ID)
    document = document_fixture(creation_info_fixture(spdx_id=DOCUMENT_ID), packages=[package], files=[file],
                                relationships=[relationship])

    # Weird type hint to make warnings about unresolved references from the mock class disappear
    relationship_converter: Union[RelationshipConverter, NonCallableMagicMock] = converter.relationship_converter
    relationship_converter.convert.return_value = "mock_converted_relationship"

    converted_dict = converter.convert(document)

    relationships = converted_dict.get(converter.json_property_name(DocumentProperty.RELATIONSHIPS))

    if should_be_written:
        assert_mock_method_called_with_arguments(relationship_converter, "convert", relationship)
        assert relationships == ["mock_converted_relationship"]
    else:
        assert_no_mock_methods_called(relationship_converter)
        assert relationships is None
