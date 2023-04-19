# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime
from typing import Union
from unittest import mock
from unittest.mock import MagicMock, NonCallableMagicMock

import pytest

from spdx_tools.spdx.jsonschema.annotation_converter import AnnotationConverter
from spdx_tools.spdx.jsonschema.document_converter import DocumentConverter
from spdx_tools.spdx.jsonschema.document_properties import DocumentProperty
from spdx_tools.spdx.model import (
    Actor,
    ActorType,
    Annotation,
    AnnotationType,
    Document,
    ExtractedLicensingInfo,
    Relationship,
    RelationshipType,
)
from tests.spdx.fixtures import (
    annotation_fixture,
    creation_info_fixture,
    external_document_ref_fixture,
    file_fixture,
    package_fixture,
    snippet_fixture,
)
from tests.spdx.mock_utils import assert_mock_method_called_with_arguments


@pytest.fixture
@mock.patch("spdx_tools.spdx.jsonschema.creation_info_converter.CreationInfoConverter", autospec=True)
@mock.patch("spdx_tools.spdx.jsonschema.external_document_ref_converter.ExternalDocumentRefConverter", autospec=True)
@mock.patch("spdx_tools.spdx.jsonschema.package_converter.PackageConverter", autospec=True)
@mock.patch("spdx_tools.spdx.jsonschema.annotation_converter.AnnotationConverter", autospec=True)
@mock.patch(
    "spdx_tools.spdx.jsonschema.extracted_licensing_info_converter.ExtractedLicensingInfoConverter", autospec=True
)
@mock.patch("spdx_tools.spdx.jsonschema.file_converter.FileConverter", autospec=True)
@mock.patch("spdx_tools.spdx.jsonschema.snippet_converter.SnippetConverter", autospec=True)
@mock.patch("spdx_tools.spdx.jsonschema.relationship_converter.RelationshipConverter", autospec=True)
def converter(
    relationship_converter_mock: MagicMock,
    snippet_converter_mock: MagicMock,
    file_converter_mock: MagicMock,
    extracted_licensing_info_converter_mock: MagicMock,
    annotation_converter_mock: MagicMock,
    package_converter_mock: MagicMock,
    external_ref_converter_mock: MagicMock,
    creation_info_converter_mock: MagicMock,
) -> DocumentConverter:
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


@pytest.mark.parametrize(
    "document_property,expected",
    [
        (DocumentProperty.SPDX_VERSION, "spdxVersion"),
        (DocumentProperty.SPDX_ID, "SPDXID"),
        (DocumentProperty.NAME, "name"),
        (DocumentProperty.DOCUMENT_NAMESPACE, "documentNamespace"),
        (DocumentProperty.DATA_LICENSE, "dataLicense"),
        (DocumentProperty.EXTERNAL_DOCUMENT_REFS, "externalDocumentRefs"),
        (DocumentProperty.COMMENT, "comment"),
        (DocumentProperty.CREATION_INFO, "creationInfo"),
        (DocumentProperty.PACKAGES, "packages"),
        (DocumentProperty.FILES, "files"),
        (DocumentProperty.SNIPPETS, "snippets"),
        (DocumentProperty.ANNOTATIONS, "annotations"),
        (DocumentProperty.RELATIONSHIPS, "relationships"),
        (DocumentProperty.HAS_EXTRACTED_LICENSING_INFOS, "hasExtractedLicensingInfos"),
    ],
)
def test_json_property_names(converter: DocumentConverter, document_property: DocumentProperty, expected: str):
    assert converter.json_property_name(document_property) == expected


def test_successful_conversion(converter: DocumentConverter):
    creation_info = creation_info_fixture(
        spdx_version="spdxVersion",
        spdx_id="spdxId",
        name="name",
        document_namespace="namespace",
        document_comment="comment",
        data_license="dataLicense",
        external_document_refs=[external_document_ref_fixture()],
    )
    document = Document(
        creation_info,
        annotations=[
            Annotation(
                "annotationId",
                AnnotationType.REVIEW,
                Actor(ActorType.PERSON, "reviewerName"),
                datetime(2022, 12, 1),
                "reviewComment",
            )
        ],
        extracted_licensing_info=[ExtractedLicensingInfo("licenseId", "licenseText")],
        relationships=[
            Relationship(creation_info.spdx_id, RelationshipType.DESCRIBES, "describedElementId"),
            Relationship("relationshipOriginId", RelationshipType.AMENDS, "relationShipTargetId"),
        ],
        packages=[package_fixture()],
        files=[file_fixture()],
        snippets=[snippet_fixture()],
    )
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
            "mock_converted_extracted_licensing_info"
        ],
        converter.json_property_name(DocumentProperty.NAME): "name",
        converter.json_property_name(DocumentProperty.SPDX_VERSION): "spdxVersion",
        converter.json_property_name(DocumentProperty.DOCUMENT_NAMESPACE): "namespace",
        converter.json_property_name(DocumentProperty.PACKAGES): ["mock_converted_package"],
        converter.json_property_name(DocumentProperty.FILES): ["mock_converted_file"],
        converter.json_property_name(DocumentProperty.SNIPPETS): ["mock_converted_snippet"],
        converter.json_property_name(DocumentProperty.RELATIONSHIPS): [
            "mock_converted_relationship",
            "mock_converted_relationship",
        ],
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
    annotations = [
        annotation_fixture(spdx_id=file.spdx_id),
        annotation_fixture(spdx_id=package.spdx_id),
        annotation_fixture(spdx_id=snippet.spdx_id),
        document_annotation,
        other_annotation,
    ]
    document = Document(
        creation_info_fixture(spdx_id=document_id),
        files=[file],
        packages=[package],
        snippets=[snippet],
        annotations=annotations,
    )

    # Weird type hint to make warnings about unresolved references from the mock class disappear
    annotation_converter: Union[AnnotationConverter, NonCallableMagicMock] = converter.annotation_converter
    annotation_converter.convert.return_value = "mock_converted_annotation"

    converted_dict = converter.convert(document)

    assert_mock_method_called_with_arguments(annotation_converter, "convert", document_annotation, other_annotation)
    converted_document_annotations = converted_dict.get(converter.json_property_name(DocumentProperty.ANNOTATIONS))
    assert converted_document_annotations == ["mock_converted_annotation", "mock_converted_annotation"]
