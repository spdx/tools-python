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
from spdx_tools.spdx.jsonschema.snippet_converter import SnippetConverter
from spdx_tools.spdx.jsonschema.snippet_properties import SnippetProperty
from spdx_tools.spdx.model import (
    Actor,
    ActorType,
    Annotation,
    AnnotationType,
    Document,
    Snippet,
    SpdxNoAssertion,
    SpdxNone,
)
from spdx_tools.spdx.model.spdx_no_assertion import SPDX_NO_ASSERTION_STRING
from spdx_tools.spdx.model.spdx_none import SPDX_NONE_STRING
from tests.spdx.fixtures import annotation_fixture, creation_info_fixture, document_fixture, snippet_fixture
from tests.spdx.mock_utils import assert_mock_method_called_with_arguments


@pytest.fixture
@mock.patch("spdx_tools.spdx.jsonschema.annotation_converter.AnnotationConverter", autospec=True)
def converter(annotation_converter_mock: MagicMock) -> SnippetConverter:
    converter = SnippetConverter()
    converter.annotation_converter = annotation_converter_mock()
    return converter


@pytest.mark.parametrize(
    "snippet_property,expected",
    [
        (SnippetProperty.SPDX_ID, "SPDXID"),
        (SnippetProperty.ANNOTATIONS, "annotations"),
        (SnippetProperty.ATTRIBUTION_TEXTS, "attributionTexts"),
        (SnippetProperty.COMMENT, "comment"),
        (SnippetProperty.COPYRIGHT_TEXT, "copyrightText"),
        (SnippetProperty.LICENSE_COMMENTS, "licenseComments"),
        (SnippetProperty.LICENSE_CONCLUDED, "licenseConcluded"),
        (SnippetProperty.LICENSE_INFO_IN_SNIPPETS, "licenseInfoInSnippets"),
        (SnippetProperty.NAME, "name"),
        (SnippetProperty.RANGES, "ranges"),
        (SnippetProperty.SNIPPET_FROM_FILE, "snippetFromFile"),
    ],
)
def test_json_property_names(converter: SnippetConverter, snippet_property: SnippetProperty, expected: str):
    assert converter.json_property_name(snippet_property) == expected


def test_json_type(converter: SnippetConverter):
    assert converter.get_json_type() == SnippetProperty


def test_data_model_type(converter: SnippetConverter):
    assert converter.get_data_model_type() == Snippet


def test_successful_conversion(converter: SnippetConverter):
    converter.annotation_converter.convert.return_value = "mock_converted_annotation"
    file_spdx_id = "fileSpdxId"
    snippet = Snippet(
        "spdxId",
        file_spdx_id=file_spdx_id,
        byte_range=(1, 2),
        line_range=(3, 4),
        license_concluded=Licensing().parse("MIT and GPL-2.0"),
        license_info_in_snippet=[Licensing().parse("MIT"), Licensing().parse("GPL-2.0")],
        license_comment="licenseComment",
        copyright_text="copyrightText",
        comment="comment",
        name="name",
        attribution_texts=["attributionText1", "attributionText2"],
    )

    annotation = Annotation(
        snippet.spdx_id,
        AnnotationType.OTHER,
        Actor(ActorType.PERSON, "annotatorName"),
        datetime(2022, 12, 5),
        "other comment",
    )
    document = Document(creation_info_fixture(), snippets=[snippet], annotations=[annotation])
    converted_dict = converter.convert(snippet, document)

    assert converted_dict == {
        converter.json_property_name(SnippetProperty.SPDX_ID): "spdxId",
        converter.json_property_name(SnippetProperty.ANNOTATIONS): ["mock_converted_annotation"],
        converter.json_property_name(SnippetProperty.ATTRIBUTION_TEXTS): ["attributionText1", "attributionText2"],
        converter.json_property_name(SnippetProperty.COMMENT): "comment",
        converter.json_property_name(SnippetProperty.COPYRIGHT_TEXT): "copyrightText",
        converter.json_property_name(SnippetProperty.LICENSE_COMMENTS): "licenseComment",
        converter.json_property_name(SnippetProperty.LICENSE_CONCLUDED): "MIT AND GPL-2.0",
        converter.json_property_name(SnippetProperty.LICENSE_INFO_IN_SNIPPETS): ["MIT", "GPL-2.0"],
        converter.json_property_name(SnippetProperty.NAME): "name",
        converter.json_property_name(SnippetProperty.RANGES): [
            {
                "startPointer": {"reference": file_spdx_id, "offset": 1},
                "endPointer": {"reference": file_spdx_id, "offset": 2},
            },
            {
                "startPointer": {"reference": file_spdx_id, "lineNumber": 3},
                "endPointer": {"reference": file_spdx_id, "lineNumber": 4},
            },
        ],
        converter.json_property_name(SnippetProperty.SNIPPET_FROM_FILE): file_spdx_id,
    }


def test_null_values(converter: SnippetConverter):
    snippet = snippet_fixture(
        license_concluded=None,
        license_comment=None,
        copyright_text=None,
        comment=None,
        name=None,
        attribution_texts=[],
        license_info_in_snippet=[],
    )

    document = Document(creation_info_fixture(), snippets=[snippet])
    converted_dict = converter.convert(snippet, document)

    assert converter.json_property_name(SnippetProperty.LICENSE_CONCLUDED) not in converted_dict
    assert converter.json_property_name(SnippetProperty.LICENSE_COMMENTS) not in converted_dict
    assert converter.json_property_name(SnippetProperty.COPYRIGHT_TEXT) not in converted_dict
    assert converter.json_property_name(SnippetProperty.COMMENT) not in converted_dict
    assert converter.json_property_name(SnippetProperty.NAME) not in converted_dict
    assert converter.json_property_name(SnippetProperty.ANNOTATIONS) not in converted_dict
    assert converter.json_property_name(SnippetProperty.ATTRIBUTION_TEXTS) not in converted_dict
    assert converter.json_property_name(SnippetProperty.LICENSE_INFO_IN_SNIPPETS) not in converted_dict


def test_spdx_no_assertion(converter: SnippetConverter):
    snippet = snippet_fixture(license_concluded=SpdxNoAssertion(), license_info_in_snippet=[SpdxNoAssertion()])

    document = Document(creation_info_fixture(), snippets=[snippet])
    converted_dict = converter.convert(snippet, document)

    assert converted_dict[converter.json_property_name(SnippetProperty.LICENSE_CONCLUDED)] == SPDX_NO_ASSERTION_STRING
    assert converted_dict[converter.json_property_name(SnippetProperty.LICENSE_INFO_IN_SNIPPETS)] == [
        SPDX_NO_ASSERTION_STRING
    ]


def test_spdx_none(converter: SnippetConverter):
    snippet = snippet_fixture(license_concluded=SpdxNone(), license_info_in_snippet=[SpdxNone()])

    document = Document(creation_info_fixture(), snippets=[snippet])
    converted_dict = converter.convert(snippet, document)

    assert converted_dict[converter.json_property_name(SnippetProperty.LICENSE_CONCLUDED)] == SPDX_NONE_STRING
    assert converted_dict[converter.json_property_name(SnippetProperty.LICENSE_INFO_IN_SNIPPETS)] == [SPDX_NONE_STRING]


def test_snippet_annotations(converter: SnippetConverter):
    snippet = snippet_fixture(spdx_id="snippetId")
    document = document_fixture(snippets=[snippet])
    first_snippet_annotation = annotation_fixture(spdx_id=snippet.spdx_id)
    second_snippet_annotation = annotation_fixture(spdx_id=snippet.spdx_id)
    document_annotation = annotation_fixture(spdx_id=document.creation_info.spdx_id)
    package_annotation = annotation_fixture(spdx_id=document.packages[0].spdx_id)
    file_annotation = annotation_fixture(spdx_id=document.files[0].spdx_id)
    other_annotation = annotation_fixture(spdx_id="otherId")
    annotations = [
        first_snippet_annotation,
        second_snippet_annotation,
        document_annotation,
        package_annotation,
        file_annotation,
        other_annotation,
    ]
    document.annotations = annotations

    # Weird type hint to make warnings about unresolved references from the mock class disappear
    annotation_converter: Union[AnnotationConverter, NonCallableMagicMock] = converter.annotation_converter
    annotation_converter.convert.return_value = "mock_converted_annotation"

    converted_dict = converter.convert(snippet, document)

    assert_mock_method_called_with_arguments(
        annotation_converter, "convert", first_snippet_annotation, second_snippet_annotation
    )
    converted_file_annotations = converted_dict.get(converter.json_property_name(SnippetProperty.ANNOTATIONS))
    assert converted_file_annotations == ["mock_converted_annotation", "mock_converted_annotation"]
