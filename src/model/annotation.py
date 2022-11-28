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
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto

from typeguard import typechecked

from src.model.dataclass_with_properties import dataclass_with_properties


class AnnotationType(Enum):
    REVIEW = auto()
    OTHER = auto()


@typechecked
@dataclass_with_properties
@dataclass(eq=True)
class Annotation:
    spdx_id: str
    annotation_type: AnnotationType
    annotator: str
    annotation_date: datetime
    annotation_comment: str
