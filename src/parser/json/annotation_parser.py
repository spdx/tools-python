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

from src.model.actor import Actor
from src.model.annotation import Annotation, AnnotationType
from src.parser.error import SPDXParsingError
from src.parser.json.actor_parser import ActorParser
from src.parser.json.dict_parsing_functions import datetime_from_str, construct_or_raise_parsing_error, \
    parse_field_or_log_error, append_parsed_field_or_log_error, raise_parsing_error_if_logger_has_messages
from src.parser.logger import Logger


class AnnotationParser:
    logger: Logger
    actor_parser: ActorParser

    def __init__(self):
        self.logger = Logger()
        self.actor_parser = ActorParser()

    def parse_all_annotations(self, input_doc_dict: Dict) -> List[Annotation]:
        annotations_list = []
        self.parse_annotations_from_object(annotations_list, [input_doc_dict])
        reviews: List[Dict] = input_doc_dict.get("revieweds")
        if reviews:
            for review in reviews:
                annotations_list = append_parsed_field_or_log_error(
                    list_to_append_to=annotations_list, logger=self.logger, field=review,
                    method_to_parse=lambda x: self.parse_review(x, spdx_id=input_doc_dict.get("SPDXID")))

        packages: List[Dict] = input_doc_dict.get("packages")
        self.parse_annotations_from_object(annotations_list, packages)
        files: List[Dict] = input_doc_dict.get("files")
        self.parse_annotations_from_object(annotations_list, files)
        snippets: List[Dict] = input_doc_dict.get("snippets")
        self.parse_annotations_from_object(annotations_list, snippets)

        raise_parsing_error_if_logger_has_messages(self.logger, "Annotations")
        return annotations_list

    def parse_annotations_from_object(self, annotations_list, element_list: List[Dict]):
        if element_list:
            for element in element_list:
                element_spdx_id: str = element.get("SPDXID")
                element_annotations: List[Dict] = element.get("annotations")
                if element_annotations:
                    annotations_list.extend(parse_field_or_log_error(
                        logger=self.logger, field=element_annotations,
                        parsing_method=lambda x: self.parse_annotations(x, spdx_id=element_spdx_id),
                        default=[]))

    def parse_annotations(self, annotations_dict_list: List[Dict], spdx_id: Optional[str] = None) -> List[Annotation]:
        logger = Logger()
        annotations_list = []
        for annotation_dict in annotations_dict_list:
            annotations_list = append_parsed_field_or_log_error(
                list_to_append_to=annotations_list,
                logger=self.logger,
                field=annotation_dict,
                method_to_parse=lambda x: self.parse_annotation(x, spdx_id=spdx_id))
        raise_parsing_error_if_logger_has_messages(logger, "Annotations")

        return annotations_list

    def parse_annotation(self, annotation: Dict, spdx_id: Optional[str] = None) -> Annotation:
        logger = Logger()
        spdx_id: str = annotation.get("SPDXID") or spdx_id

        annotation_type: Optional[AnnotationType] = parse_field_or_log_error(logger=logger,
                                                                             field=annotation.get("annotationType"),
                                                                             parsing_method=self.parse_annotation_type)

        annotator: Optional[Actor] = parse_field_or_log_error(logger=logger, field=annotation.get("annotator"),
                                                              parsing_method=self.actor_parser.parse_actor)

        annotation_date: Optional[datetime] = parse_field_or_log_error(logger=logger,
                                                                       field=annotation.get("annotationDate"),
                                                                       parsing_method=datetime_from_str)

        annotation_comment: str = annotation.get("comment")
        raise_parsing_error_if_logger_has_messages(logger, "Annotation")
        annotation = construct_or_raise_parsing_error(Annotation,
                                                      dict(spdx_id=spdx_id, annotation_type=annotation_type,
                                                           annotator=annotator, annotation_date=annotation_date,
                                                           annotation_comment=annotation_comment))

        return annotation

    @staticmethod
    def parse_annotation_type(annotation_type: str) -> AnnotationType:
        try:
            return AnnotationType[annotation_type]
        except KeyError:
            raise SPDXParsingError([f"Invalid annotation type: {annotation_type}"])

    def parse_review(self, review_dict: Dict, spdx_id: str) -> Annotation:
        logger = Logger()
        annotator: Optional[Actor] = parse_field_or_log_error(logger=logger,
                                                              field=review_dict.get("reviewer"),
                                                              parsing_method=self.actor_parser.parse_actor,
                                                              optional=True)

        annotation_date: Optional[datetime] = parse_field_or_log_error(logger=logger, field=review_dict.get("reviewDate"),
                                                                       parsing_method=datetime_from_str)

        annotation_type = AnnotationType.REVIEW
        comment: str = review_dict.get("comment")
        raise_parsing_error_if_logger_has_messages(logger, "Review")

        annotation = construct_or_raise_parsing_error(Annotation,
                                                      dict(spdx_id=spdx_id, annotation_type=annotation_type,
                                                           annotator=annotator, annotation_date=annotation_date,
                                                           annotation_comment=comment))
        return annotation
