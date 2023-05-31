# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from datetime import datetime
from unittest import mock

from spdx_tools.spdx.model import Annotation, AnnotationType


@mock.patch("spdx_tools.spdx.model.Actor", autospec=True)
def test_correct_initialization(actor):
    annotation = Annotation("id", AnnotationType.OTHER, actor, datetime(2022, 1, 1), "comment")
    assert annotation.spdx_id == "id"
    assert annotation.annotation_type == AnnotationType.OTHER
    assert annotation.annotator == actor
    assert annotation.annotation_date == datetime(2022, 1, 1)
    assert annotation.annotation_comment == "comment"
