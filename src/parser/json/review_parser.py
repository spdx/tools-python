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
from typing import Dict, List

from src.model.annotation import Annotation, AnnotationType
from src.parser.logger import Logger


class ReviewParser:  # direkt AnnotationParser benutzen mit annotation_type als Argument?
    logger: Logger

    def __init__(self, logger: Logger):
        self.logger = logger

    def parse_review(self, review: Dict) -> Annotation:
        annotation_date = review.get("reviewDate")
        annotator = review.get("reviewer")
        try:
            annotation = Annotation(annotation_type=AnnotationType.REVIEW, annotator=annotator,
                                annotation_date=annotation_date)
        except ValueError as error:
            self.logger.append(error.args[0])
        return annotation

    def parse_reviews(self, review_dicts_list: List[Dict]) -> List[Annotation]:
        reviews_list = []
        for review_dict in review_dicts_list:
            reviews_list.append(self.parse_review(review_dict))
        return reviews_list
