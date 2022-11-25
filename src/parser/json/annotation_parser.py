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
from typing import Dict, Optional, List

from src.model.annotation import Annotation, AnnotationType
from src.model.typing.constructor_type_errors import ConstructorTypeErrors
from src.parser.error import SPDXParsingError
from src.parser.json.actor_parser import ActorParser
from src.parser.json.dict_parsing_functions import datetime_from_str
from src.parser.logger import Logger


class AnnotationParser:
    logger: Logger
    actor_parser: ActorParser

    def __init__(self):
        self.logger = Logger()
        self.actor_parser = ActorParser()

    def parse_annotation(self, annotation: Dict, spdx_id: Optional[str] = None) -> Annotation:

        spdx_id = annotation.get("SPDXID") or spdx_id
        annotation_type = self.parse_annotation_type(annotation.get("annotationType"))
        annotator = self.actor_parser.parse_actor(annotation.get("annotator"))
        annotation_date = datetime_from_str(annotation.get("annotationDate"))
        annotation_comment = annotation.get("comment")
        try:
            annotation = Annotation(spdx_id, annotation_type, annotator, annotation_date, annotation_comment)
        except ConstructorTypeErrors as err:
            raise SPDXParsingError(err.get_messages())
        return annotation

    def parse_annotation_type(self, annotation_type: str) -> AnnotationType:
        try:
            return AnnotationType[annotation_type]
        except KeyError:
            self.logger.append(f"Invalid annotation type: {annotation_type}")

    def parse_annotations(self, annotations_dict_list: List[Dict], spdx_id: Optional[str] = None) -> List[Annotation]:
        annotations_list = []
        for annotation_dict in annotations_dict_list:
            try:
                annotation = self.parse_annotation(annotation_dict, spdx_id=spdx_id)
                annotations_list.append(annotation)
            except SPDXParsingError as err:
                self.logger.append_all(err.get_messages())

        return annotations_list

    def parse_all_annotations(self, input_doc_dict: Dict):
        annotations_list = []
        doc_spdx_id = input_doc_dict.get("SPDXID")
        document_annotations = input_doc_dict.get("annotations")
        if document_annotations:
            annotations_list.extend(self.parse_annotations(document_annotations, spdx_id=doc_spdx_id))
        packages = input_doc_dict.get("packages")
        if packages:
            for package in packages:
                package_spdx_id = package.get("SPDXID")
                package_annotations = package.get("annotations")
                if package_annotations:
                    annotations_list.extend(self.parse_annotations(package_annotations, spdx_id=package_spdx_id))
        files = input_doc_dict.get("files")
        if files:
            for file in files:
                file_spdx_id = file.get("SPDXID")
                file_annotations = file.get("annotations")
                if file_annotations:
                    annotations_list.extend(self.parse_annotations(file_annotations, spdx_id=file_spdx_id))

        snippets = input_doc_dict.get("snippets")
        if snippets:
            for snippet in snippets:
                snippet_spdx_id = snippet.get("SPDXID")
                snippet_annotations = snippet.get("annotations")
                if snippet_annotations:
                    annotations_list.extend(self.parse_annotations(snippet_annotations, spdx_id=snippet_spdx_id))

        reviews = input_doc_dict.get("revieweds")
        if reviews:
            for review in reviews:
                review_annotation = self.parse_review(review, doc_spdx_id)
                if review_annotation:
                    annotations_list.append(review_annotation)
        if self.logger.has_messages():
            raise SPDXParsingError(self.logger.get_messages())
        return annotations_list


    def parse_review(self, review_dict: Dict, spdx_id: str) -> Optional[Annotation]:
        annotator = self.actor_parser.parse_actor(review_dict.get("reviewer"))
        annotation_date = datetime_from_str(review_dict.get("reviewDate"))
        annotation_type = AnnotationType.REVIEW
        comment = review_dict.get("comment")

        try:
            return Annotation(spdx_id=spdx_id, annotator=annotator, annotation_date=annotation_date,
                          annotation_type=annotation_type, annotation_comment=comment)
        except ConstructorTypeErrors as err:
            self.logger.append_all(err.get_messages())
            return None
