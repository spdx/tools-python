# Copyright (c) 2023 spdx contributors
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

import pytest

from spdx.parser.tagvalue.parser.tagvalue import Parser
from tests.spdx.parser.tagvalue.test_creation_info_parser import DOCUMENT_STR

from spdx.model.annotation import AnnotationType


@pytest.fixture
def parser():
    spdx_parser = Parser()
    spdx_parser.build()
    return spdx_parser


def test_annotation(parser):
    annotation_str = '\n'.join([
        'Annotator: Person: Jane Doe()',
        'AnnotationDate: 2010-01-29T18:30:22Z',
        'AnnotationComment: <text>Document level annotation</text>',
        'AnnotationType: OTHER',
        'SPDXREF: SPDXRef-DOCUMENT'
    ])
    document = parser.parse("\n".join([DOCUMENT_STR, annotation_str]))
    assert document is not None
    assert len(document.annotations) == 1
    annotation = document.annotations[0]
    assert annotation.annotator.name == 'Jane Doe'
    assert annotation.annotation_date == datetime(2010, 1, 29, 18, 30, 22)
    assert annotation.annotation_comment == 'Document level annotation'
    assert annotation.annotation_type == AnnotationType.OTHER
    assert annotation.spdx_id == 'SPDXRef-DOCUMENT'
