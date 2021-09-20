# Copyright (c) 2018 Yash M. Nisar
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
from functools import total_ordering

from spdx.utils import datetime_iso_format


@total_ordering
class Annotation(object):

    """
    Document annotation information.
    Fields:
    - annotator: Person, Organization or tool that has commented on a file,
    package, or the entire document. Conditional (Mandatory, one), if there
    is an Annotation.
    - annotation_date: To identify when the comment was made. Conditional
    (Mandatory, one), if there is an Annotation. Type: datetime.
    - comment: Annotation comment. Conditional (Mandatory, one), if there is
    an Annotation. Type: str.
    - annotation_type: Annotation type. Conditional (Mandatory, one), if there is an
    Annotation. Type: str.
    - spdx_id: Uniquely identify the element in an SPDX document which is being
    referenced. Conditional (Mandatory, one), if there is an Annotation.
    Type: str.
    """

    def __init__(
        self,
        annotator=None,
        annotation_date=None,
        comment=None,
        annotation_type=None,
        spdx_id=None,
    ):
        self.annotator = annotator
        self.annotation_date = annotation_date
        self.comment = comment
        self.annotation_type = annotation_type
        self.spdx_id = spdx_id

    def __eq__(self, other):
        return (
            isinstance(other, Annotation)
            and self.annotator == other.annotator
            and self.annotation_date == other.annotation_date
            and self.comment == other.comment
        )

    def __lt__(self, other):
        return (self.annotator, self.annotation_date, self.comment) < (
            other.annotator,
            other.annotation_date,
            other.comment,
        )

    def set_annotation_date_now(self):
        self.annotation_date = datetime.utcnow()

    @property
    def annotation_date_iso_format(self):
        return datetime_iso_format(self.annotation_date)

    @property
    def has_comment(self):
        return self.comment is not None

    def validate(self, messages):
        """
        Check that all the fields are valid.
        Appends any error messages to messages parameter shall be a ErrorMessages.
        """
        self.validate_annotator(messages)
        self.validate_annotation_date(messages)
        self.validate_annotation_type(messages)
        self.validate_spdx_id(messages)

    def validate_annotator(self, messages):
        if self.annotator is None:
            messages.append("Annotation missing annotator.")

    def validate_annotation_date(self, messages):
        if self.annotation_date is None:
            messages.append("Annotation missing annotation date.")

    def validate_annotation_type(self, messages):
        if self.annotation_type is None:
            messages.append("Annotation missing annotation type.")

    def validate_spdx_id(self, messages):
        if self.spdx_id is None:
            messages.append("Annotation missing SPDX Identifier Reference.")
