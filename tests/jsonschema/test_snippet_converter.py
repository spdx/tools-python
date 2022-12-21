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

from src.jsonschema.snippet_converter import SnippetConverter
from src.jsonschema.snippet_properties import SnippetProperty
from src.model.actor import Actor, ActorType
from src.model.annotation import Annotation, AnnotationType
from src.model.document import Document
from src.model.license_expression import LicenseExpression
from src.model.snippet import Snippet
from src.model.spdx_no_assertion import SpdxNoAssertion, SPDX_NO_ASSERTION_STRING
from src.model.spdx_none import SpdxNone, SPDX_NONE_STRING
from tests.fixtures import creation_info_fixture, snippet_fixture


@pytest.fixture
@mock.patch('src.jsonschema.annotation_converter.AnnotationConverter', autospec=True)
def converter(annotation_converter_mock: MagicMock) -> SnippetConverter:
    converter = SnippetConverter()
    converter.annotation_converter = annotation_converter_mock()
    return converter


@pytest.mark.parametrize("snippet_property,expected",
                         [(SnippetProperty.SPDX_ID, "SPDXID"),
                          (SnippetProperty.ANNOTATIONS, "annotations"),
                          (SnippetProperty.ATTRIBUTION_TEXTS, "attributionTexts"),
                          (SnippetProperty.COMMENT, "comment"),
                          (SnippetProperty.COPYRIGHT_TEXT, "copyrightText"),
                          (SnippetProperty.LICENSE_COMMENTS, "licenseComments"),
                          (SnippetProperty.LICENSE_CONCLUDED, "licenseConcluded"),
                          (SnippetProperty.LICENSE_INFO_IN_SNIPPETS, "licenseInfoInSnippets"),
                          (SnippetProperty.NAME, "name"),
                          (SnippetProperty.RANGES, "ranges"),
                          (SnippetProperty.SNIPPET_FROM_FILE, "snippetFromFile")])
def test_json_property_names(converter: SnippetConverter, snippet_property: SnippetProperty,
                             expected: str):
    assert converter.json_property_name(snippet_property) == expected


def test_json_type(converter: SnippetConverter):
    assert converter.get_json_type() == SnippetProperty


def test_data_model_type(converter: SnippetConverter):
    assert converter.get_data_model_type() == Snippet


def test_successful_conversion(converter: SnippetConverter):
    converter.annotation_converter.convert.return_value = "mock_converted_annotation"
    file_spdx_id = "fileSpdxId"
    snippet = Snippet("spdxId", file_spdx_id=file_spdx_id, byte_range=(1, 2), line_range=(3, 4),
                      concluded_license=LicenseExpression("licenseExpression1"),
                      license_info_in_snippet=[LicenseExpression("licenseExpression2"),
                                               LicenseExpression("licenseExpression3")],
                      license_comment="licenseComment", copyright_text="copyrightText", comment="comment", name="name",
                      attribution_texts=["attributionText1", "attributionText2"])

    annotation = Annotation(snippet.spdx_id, AnnotationType.OTHER, Actor(ActorType.PERSON, "annotatorName"),
                            datetime(2022, 12, 5), "other comment")
    document = Document(creation_info_fixture(), snippets=[snippet], annotations=[annotation])
    converted_dict = converter.convert(snippet, document)

    assert converted_dict[converter.json_property_name(SnippetProperty.SPDX_ID)] == "spdxId"
    assert converted_dict[converter.json_property_name(SnippetProperty.ANNOTATIONS)] == ["mock_converted_annotation"]
    assert converted_dict[converter.json_property_name(SnippetProperty.ATTRIBUTION_TEXTS)] == ["attributionText1",
                                                                                               "attributionText2"]
    assert converted_dict[converter.json_property_name(SnippetProperty.COMMENT)] == "comment"
    assert converted_dict[converter.json_property_name(SnippetProperty.COPYRIGHT_TEXT)] == "copyrightText"
    assert converted_dict[converter.json_property_name(SnippetProperty.LICENSE_COMMENTS)] == "licenseComment"
    assert converted_dict[converter.json_property_name(SnippetProperty.LICENSE_CONCLUDED)] == "licenseExpression1"
    assert converted_dict[converter.json_property_name(SnippetProperty.LICENSE_INFO_IN_SNIPPETS)] == [
        "licenseExpression2", "licenseExpression3"]
    assert converted_dict[converter.json_property_name(SnippetProperty.NAME)] == "name"
    assert converted_dict[converter.json_property_name(SnippetProperty.RANGES)] == [
        {"startPointer": {"reference": file_spdx_id, "offset": 1},
         "endPointer": {"reference": file_spdx_id, "offset": 2}},
        {"startPointer": {"reference": file_spdx_id, "lineNumber": 3},
         "endPointer": {"reference": file_spdx_id, "lineNumber": 4}}]
    assert converted_dict[converter.json_property_name(SnippetProperty.SNIPPET_FROM_FILE)] == file_spdx_id


def test_null_values(converter: SnippetConverter):
    snippet = snippet_fixture(concluded_license=None, license_comment=None, copyright_text=None, comment=None,
                              name=None)

    document = Document(creation_info_fixture(), snippets=[snippet])
    converted_dict = converter.convert(snippet, document)

    assert converter.json_property_name(SnippetProperty.LICENSE_CONCLUDED) not in converted_dict
    assert converter.json_property_name(SnippetProperty.LICENSE_COMMENTS) not in converted_dict
    assert converter.json_property_name(SnippetProperty.COPYRIGHT_TEXT) not in converted_dict
    assert converter.json_property_name(SnippetProperty.COMMENT) not in converted_dict
    assert converter.json_property_name(SnippetProperty.NAME) not in converted_dict


def test_spdx_no_assertion(converter: SnippetConverter):
    snippet = snippet_fixture(concluded_license=SpdxNoAssertion(), license_info_in_snippet=SpdxNoAssertion())

    document = Document(creation_info_fixture(), snippets=[snippet])
    converted_dict = converter.convert(snippet, document)

    assert converted_dict[converter.json_property_name(SnippetProperty.LICENSE_CONCLUDED)] == SPDX_NO_ASSERTION_STRING
    assert converted_dict[
               converter.json_property_name(SnippetProperty.LICENSE_INFO_IN_SNIPPETS)] == SPDX_NO_ASSERTION_STRING


def test_spdx_none(converter: SnippetConverter):
    snippet = snippet_fixture(concluded_license=SpdxNone(), license_info_in_snippet=SpdxNone())

    document = Document(creation_info_fixture(), snippets=[snippet])
    converted_dict = converter.convert(snippet, document)

    assert converted_dict[converter.json_property_name(SnippetProperty.LICENSE_CONCLUDED)] == SPDX_NONE_STRING
    assert converted_dict[
               converter.json_property_name(SnippetProperty.LICENSE_INFO_IN_SNIPPETS)] == SPDX_NONE_STRING
