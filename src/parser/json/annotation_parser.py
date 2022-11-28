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
from src.parser.logger import Logger


class AnnotationParser:
    logger: Logger

    def __init__(self, logger):
        self.logger = logger

    def parse_annotation(self, annotation: Dict, spdx_id: Optional[str] = None) -> Annotation:
        try:
            spdx_id = annotation.get("SPDXID") or spdx_id
            annotation_type = annotation.get("annotationType")
            annotator = annotation.get("annotator")
            annotation_date = annotation.get("annotationDate")
            annotation_comment = annotation.get("annotationComment")
            annotation = Annotation(spdx_id, annotation_type, annotator, annotation_date, annotation_comment)
        except ValueError as err:
            self.logger.append(f'Error while parsing annotation: {err.args[0]}')
        return annotation

    def parse_annotations(self, annotations_dict_list: List[Dict], spdx_id: Optional[str] = None) -> List[Annotation]:
        annotations_list = []
        for annotation_dict in annotations_dict_list:
            annotations_list.append(self.parse_annotation(annotation_dict, spdx_id))
        return annotations_list
