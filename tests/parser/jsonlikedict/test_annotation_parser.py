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
import datetime
from unittest import TestCase

import pytest

from spdx.model.actor import Actor, ActorType
from spdx.model.annotation import AnnotationType, Annotation
from spdx.parser.error import SPDXParsingError
from spdx.parser.jsonlikedict.annotation_parser import AnnotationParser


def test_parse_annotation():
    annotation_parser = AnnotationParser()
    annotation_dict = {
        "annotationDate": "2010-01-29T18:30:22Z",
        "annotationType": "OTHER",
        "annotator": "Person: Jane Doe ()",
        "comment": "Document level annotation"
    }

    annotation = annotation_parser.parse_annotation(annotation_dict, spdx_id="SPDXRef-DOCUMENT")

    assert annotation.annotator == Actor(ActorType.PERSON, name="Jane Doe")
    assert annotation.annotation_type == AnnotationType.OTHER
    assert annotation.annotation_date == datetime.datetime(2010, 1, 29, 18, 30, 22)
    assert annotation.annotation_comment == "Document level annotation"
    assert annotation.spdx_id == "SPDXRef-DOCUMENT"


def test_parse_all_annotations():
    annotation_parser = AnnotationParser()
    doc_dict = {
        "SPDXID": "SPDXRef-DOCUMENT",
        "packages": [
            {"SPDXID": "SPDXRef-Package",
             "annotations": [
                 {"annotationDate": "2010-01-29T17:30:22Z",
                  "annotationType": "REVIEW",
                  "annotator": "Person: Mick Doe ()",
                  "comment": "Package level annotation"}
             ]}],
        "files": [
            {"SPDXID": "SPDXRef-File",
             "annotations": [
                 {"annotationDate": "2010-01-29T18:30:22Z",
                  "annotationType": "OTHER",
                  "annotator": "Person: Jane Doe ()",
                  "comment": "File level annotation"}
             ]}
        ],
        "snippets": [
            {"SPDXID": "SPDXRef-Snippet",
             "annotations": [
                 {"annotationDate": "2022-01-29T18:30:32Z",
                  "annotationType": "REVIEW",
                  "annotator": "Person: Jonas Rie (jonas@example.com)",
                  "comment": "Snippet level annotation"}
             ]}],
        "revieweds":
            [{
                "reviewDate": "2010-01-29T18:30:22Z",
                "reviewer": "Person: Jane Doe ()",
                "comment": "Review annotation"
            }]
    }

    annotations = annotation_parser.parse_all_annotations(input_doc_dict=doc_dict)

    assert len(annotations) == 4
    test_case = TestCase()
    test_case.maxDiff = None
    test_case.assertCountEqual(annotations, [Annotation(spdx_id="SPDXRef-DOCUMENT",
                                                         annotation_type=AnnotationType.REVIEW,
                                                         annotator=Actor(actor_type=ActorType.PERSON, name="Jane Doe",
                                                                         email=None),
                                                         annotation_date=datetime.datetime(2010, 1, 29, 18, 30, 22),
                                                         annotation_comment="Review annotation"),
                                              Annotation(spdx_id="SPDXRef-Package",
                                                         annotation_type=AnnotationType.REVIEW,
                                                         annotator=Actor(actor_type=ActorType.PERSON, name="Mick Doe",
                                                                         email=None),
                                                         annotation_date=datetime.datetime(2010, 1, 29, 17, 30, 22),
                                                         annotation_comment="Package level annotation"),
                                              Annotation(spdx_id="SPDXRef-File", annotation_type=AnnotationType.OTHER,
                                                         annotator=Actor(actor_type=ActorType.PERSON, name="Jane Doe",
                                                                         email=None),
                                                         annotation_date=datetime.datetime(2010, 1, 29, 18, 30, 22),
                                                         annotation_comment="File level annotation"),
                                              Annotation(spdx_id="SPDXRef-Snippet",
                                                         annotation_type=AnnotationType.REVIEW,
                                                         annotator=Actor(actor_type=ActorType.PERSON, name="Jonas Rie",
                                                                         email="jonas@example.com"),
                                                         annotation_date=datetime.datetime(2022, 1, 29, 18, 30, 32),
                                                         annotation_comment="Snippet level annotation")])


@pytest.mark.parametrize("incomplete_annotation_dict,expected_message", [({"annotator": "Person: Jane Doe ()"}, [
    "Error while constructing Annotation: ['SetterError Annotation: type of " 'argument "spdx_id" must be str; got NoneType instead: None\', \'SetterError Annotation: type of argument "annotation_type" must be ' "spdx.model.annotation.AnnotationType; got NoneType instead: None', " '\'SetterError Annotation: type of argument "annotation_date" must be ' "datetime.datetime; got NoneType instead: None', 'SetterError Annotation: " 'type of argument "annotation_comment" must be str; got NoneType instead: ' "None']"]),
                                                                         ({"annotationDate": "2010-01-29T18:30:22Z"}, ["Error while constructing Annotation: ['SetterError Annotation: type of " 'argument "spdx_id" must be str; got NoneType instead: None\', \'SetterError Annotation: type of argument "annotation_type" must be ' "spdx.model.annotation.AnnotationType; got NoneType instead: None', " '\'SetterError Annotation: type of argument "annotator" must be ' "spdx.model.actor.Actor; got NoneType instead: None', 'SetterError Annotation: " 'type of argument "annotation_comment" must be str; got NoneType instead: ' "None']"])])
def test_parse_incomplete_annotation(incomplete_annotation_dict, expected_message):
    annotation_parser = AnnotationParser()

    with pytest.raises(SPDXParsingError) as err:
        annotation_parser.parse_annotation(incomplete_annotation_dict)

    TestCase().assertCountEqual(err.value.get_messages(), expected_message)
