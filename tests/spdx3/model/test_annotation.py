# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest import mock

import pytest

from spdx3.model.annotation import Annotation, AnnotationType


@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_correct_initialization(creation_information):
    annotation = Annotation(
        "SPDXRef-Annotation",
        creation_information,
        AnnotationType.OTHER,
        "spdx_id1",
        content_type="mediaType",
        statement="This is a statement",
    )

    assert annotation.spdx_id == "SPDXRef-Annotation"
    assert annotation.creation_info == creation_information
    assert annotation.annotation_type == AnnotationType.OTHER
    assert annotation.subject == "spdx_id1"
    assert annotation.content_type == "mediaType"
    assert annotation.statement == "This is a statement"


@mock.patch("spdx3.model.creation_information.CreationInformation")
def test_invalid_initialization(creation_information):
    with pytest.raises(TypeError) as err:
        Annotation(
            "SPDXRef-Annotation",
            creation_information,
            "REVIEW",
            {"element": 1},
            content_type=4,
            statement=["some statements"],
        )

    assert err.value.args[0] == [
        'SetterError Annotation: type of argument "annotation_type" must be '
        "spdx3.model.annotation.AnnotationType; got str instead: REVIEW",
        'SetterError Annotation: type of argument "subject" must be str; got dict ' "instead: {'element': 1}",
        'SetterError Annotation: type of argument "content_type" must be one of (str, '
        "NoneType); got int instead: 4",
        'SetterError Annotation: type of argument "statement" must be one of (str, '
        "NoneType); got list instead: ['some statements']",
    ]
