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
from src.parser.json.dict_parsing_functions import datetime_from_str, try_construction_raise_parsing_error
from src.parser.logger import Logger


class AnnotationParser:
    logger: Logger
    actor_parser: ActorParser

    def __init__(self):
        self.logger = Logger()
        self.actor_parser = ActorParser()

    def parse_all_annotations(self, input_doc_dict: Dict) -> List[Annotation]:
        annotations_list = []
        doc_spdx_id: str = input_doc_dict.get("SPDXID")
        document_annotations: List[Dict] = input_doc_dict.get("annotations")
        if document_annotations:
            try:
                annotations_list.extend(self.parse_annotations(document_annotations, spdx_id=doc_spdx_id))
            except SPDXParsingError as err:
                self.logger.append_all(err.get_messages())

        reviews: List[Dict] = input_doc_dict.get("revieweds")
        if reviews:
            for review in reviews:
                try:
                    review_annotation: Annotation = self.parse_review(review, spdx_id=doc_spdx_id)
                    if review_annotation:
                        annotations_list.append(review_annotation)
                except SPDXParsingError as err:
                    self.logger.append_all(err.get_messages())
        packages: List[Dict] = input_doc_dict.get("packages")
        if packages:
            for package in packages:
                package_spdx_id: str = package.get("SPDXID")
                package_annotations: List[Dict] = package.get("annotations")
                if package_annotations:
                    try:
                        annotations_list.extend(self.parse_annotations(package_annotations, spdx_id=package_spdx_id))
                    except SPDXParsingError as err:
                        self.logger.append_all(err.get_messages())
        files: List[Dict] = input_doc_dict.get("files")
        if files:
            for file in files:
                file_spdx_id: str = file.get("SPDXID")
                file_annotations: List[Dict] = file.get("annotations")
                if file_annotations:
                    try:
                        annotations_list.extend(self.parse_annotations(file_annotations, spdx_id=file_spdx_id))
                    except SPDXParsingError as err:
                        self.logger.append_all(err.get_messages())

        snippets: List[Dict] = input_doc_dict.get("snippets")
        if snippets:
            for snippet in snippets:
                snippet_spdx_id: str = snippet.get("SPDXID")
                snippet_annotations: List[Dict] = snippet.get("annotations")
                if snippet_annotations:
                    try:
                        annotations_list.extend(self.parse_annotations(snippet_annotations, spdx_id=snippet_spdx_id))
                    except SPDXParsingError as err:
                        self.logger.append_all(err.get_messages())

        if self.logger.has_messages():
            raise SPDXParsingError(self.logger.get_messages())
        return annotations_list

    def parse_annotations(self, annotations_dict_list: List[Dict], spdx_id: Optional[str] = None) -> List[Annotation]:
        logger = Logger()
        annotations_list = []
        for annotation_dict in annotations_dict_list:
            try:
                annotation: Annotation = self.parse_annotation(annotation_dict, spdx_id=spdx_id)
                annotations_list.append(annotation)
            except SPDXParsingError as err:
                logger.append_all(err.get_messages())
        if logger.has_messages():
            raise SPDXParsingError(logger.get_messages())

        return annotations_list

    def parse_annotation(self, annotation: Dict, spdx_id: Optional[str] = None) -> Annotation:
        logger = Logger()
        spdx_id: str = annotation.get("SPDXID") or spdx_id
        try:
            annotation_type: Optional[AnnotationType] = self.parse_annotation_type(annotation.get("annotationType"))
        except SPDXParsingError as err:
            logger.append_all(err.get_messages())
            annotation_type = None
        try:
            annotator: Optional[Actor] = self.actor_parser.parse_actor(annotation.get("annotator"))
        except SPDXParsingError as err:
            logger.append_all(err.get_messages())
            annotator = None
        try:
            annotation_date: Optional[datetime] = datetime_from_str(annotation.get("annotationDate"))
        except TypeError:
            logger.append("ValueError while parsing annotationDate.")
            annotation_date = None
        annotation_comment: str = annotation.get("comment")
        if logger.has_messages():
            raise SPDXParsingError([f"Error while parsing annotation: {logger.get_messages()}"])
        annotation = try_construction_raise_parsing_error(Annotation,
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
        try:
            annotator: Optional[Actor] = self.actor_parser.parse_actor(review_dict.get("reviewer"))
        except SPDXParsingError as err:
            logger.append_all(err.get_messages())
            annotator = None
        try:
            annotation_date: Optional[datetime] = datetime_from_str(review_dict.get("reviewDate"))
        except TypeError:
            logger.append("ValueError while parsing reviewDate.")
            annotation_date = None
        annotation_type = AnnotationType.REVIEW
        comment: str = review_dict.get("comment")
        if logger.has_messages():
            raise SPDXParsingError([f"Error while parsing review: {logger.get_messages()}"])

        annotation = try_construction_raise_parsing_error(Annotation,
                                                          dict(spdx_id=spdx_id, annotation_type=annotation_type,
                                                               annotator=annotator, annotation_date=annotation_date,
                                                               annotation_comment=comment))
        return annotation
