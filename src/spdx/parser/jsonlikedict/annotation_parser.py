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
from typing import Dict, Optional, List

from spdx.model.actor import Actor
from spdx.model.annotation import Annotation, AnnotationType
from spdx.parser.error import SPDXParsingError
from spdx.parser.actor_parser import ActorParser
from spdx.parser.jsonlikedict.dict_parsing_functions import parse_field_or_log_error, append_parsed_field_or_log_error
from spdx.parser.parsing_functions import construct_or_raise_parsing_error, raise_parsing_error_if_logger_has_messages
from spdx.datetime_conversions import datetime_from_str
from spdx.parser.logger import Logger


class AnnotationParser:
    logger: Logger
    actor_parser: ActorParser

    def __init__(self):
        self.logger = Logger()
        self.actor_parser = ActorParser()

    def parse_all_annotations(self, input_doc_dict: Dict) -> List[Annotation]:
        annotations = []
        self.parse_annotations_from_object(annotations, [input_doc_dict])
        reviews: List[Dict] = input_doc_dict.get("revieweds", [])
        for review in reviews:
            annotations = append_parsed_field_or_log_error(
                self.logger, annotations, review, lambda x: self.parse_review(x, spdx_id=input_doc_dict.get("SPDXID")))
        packages: List[Dict] = input_doc_dict.get("packages", [])
        self.parse_annotations_from_object(annotations, packages)
        files: List[Dict] = input_doc_dict.get("files", [])
        self.parse_annotations_from_object(annotations, files)
        snippets: List[Dict] = input_doc_dict.get("snippets", [])
        self.parse_annotations_from_object(annotations, snippets)

        raise_parsing_error_if_logger_has_messages(self.logger, "annotations")
        return annotations

    def parse_annotations_from_object(self, annotations: List[Annotation], element_list: List[Dict]):
        for element in element_list:
            element_spdx_id: Optional[str] = element.get("SPDXID")
            element_annotations: List[Dict] = element.get("annotations", [])
            annotations.extend(parse_field_or_log_error(self.logger, element_annotations,

                                                            lambda y: self.parse_annotation(y, spdx_id=element_spdx_id),
                                                            [], True))

    def parse_annotation(self, annotation_dict: Dict, spdx_id: Optional[str] = None) -> Annotation:
        logger = Logger()
        spdx_id: Optional[str] = annotation_dict.get("SPDXID") or spdx_id

        annotation_type: Optional[AnnotationType] = parse_field_or_log_error(logger,
                                                                             annotation_dict.get("annotationType"),
                                                                             self.parse_annotation_type)

        annotator: Optional[Actor] = parse_field_or_log_error(logger, annotation_dict.get("annotator"),
                                                              self.actor_parser.parse_actor)

        annotation_date: Optional[datetime] = parse_field_or_log_error(logger, annotation_dict.get("annotationDate"),
                                                                       datetime_from_str)

        annotation_comment: Optional[str] = annotation_dict.get("comment")
        raise_parsing_error_if_logger_has_messages(logger, "Annotation")
        annotation_dict = construct_or_raise_parsing_error(Annotation,
                                                           dict(spdx_id=spdx_id, annotation_type=annotation_type,
                                                                annotator=annotator, annotation_date=annotation_date,
                                                                annotation_comment=annotation_comment))

        return annotation_dict

    @staticmethod
    def parse_annotation_type(annotation_type: str) -> AnnotationType:
        try:
            return AnnotationType[annotation_type]
        except KeyError:
            raise SPDXParsingError([f"Invalid AnnotationType: {annotation_type}"])

    def parse_review(self, review_dict: Dict, spdx_id: str) -> Annotation:
        logger = Logger()
        annotator: Optional[Actor] = parse_field_or_log_error(logger, review_dict.get("reviewer"),
                                                              self.actor_parser.parse_actor)

        annotation_date: Optional[datetime] = parse_field_or_log_error(logger, review_dict.get("reviewDate"),
                                                                       datetime_from_str)

        annotation_type = AnnotationType.REVIEW
        comment: Optional[str] = review_dict.get("comment")
        raise_parsing_error_if_logger_has_messages(logger, "Annotation from revieweds")

        annotation = construct_or_raise_parsing_error(Annotation,
                                                      dict(spdx_id=spdx_id, annotation_type=annotation_type,
                                                           annotator=annotator, annotation_date=annotation_date,
                                                           annotation_comment=comment))
        return annotation
