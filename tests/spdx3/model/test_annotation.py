# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from unittest import mock

import pytest

from spdx3.model.annotation import Annotation, AnnotationType


@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_correct_initialization(creation_information):
    annotation = Annotation("SPDXRef-Annotation", creation_information, AnnotationType.OTHER, ["spdx_id1"],
                            content_type="mediaType", statement="This is a statement")

    assert annotation.spdx_id == "SPDXRef-Annotation"
    assert annotation.creation_info == creation_information
    assert annotation.annotation_type == AnnotationType.OTHER
    assert annotation.subject == ["spdx_id1"]
    assert annotation.content_type == "mediaType"
    assert annotation.statement == "This is a statement"


@mock.patch("spdx3.model.creation_information.CreationInformation")
def test_invalid_initialization(creation_information):
    with pytest.raises(TypeError) as err:
        Annotation("SPDXRef-Annotation", creation_information, "REVIEW", {"element": 1}, content_type=4,
                   statement=["some statements"])

    assert err.value.args[0] == ['SetterError Annotation: type of argument "annotation_type" must be '
                                 'spdx3.model.annotation.AnnotationType; got str instead: REVIEW',
                                 'SetterError Annotation: type of argument "subject" must be a list; got dict '
                                 "instead: {'element': 1}",
                                 'SetterError Annotation: type of argument "content_type" must be one of (str, '
                                 'NoneType); got int instead: 4',
                                 'SetterError Annotation: type of argument "statement" must be one of (str, '
                                 "NoneType); got list instead: ['some statements']"]
