# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest.mock import MagicMock, call, mock_open, patch

from spdx_tools.spdx.writer.tagvalue.annotation_writer import write_annotation
from tests.spdx.fixtures import annotation_fixture


def test_annotation_writer():
    annotation = annotation_fixture()

    mock: MagicMock = mock_open()
    with patch(f"{__name__}.open", mock, create=True):
        with open("foo", "w") as file:
            write_annotation(annotation, file)

    mock.assert_called_once_with("foo", "w")
    handle = mock()
    handle.write.assert_has_calls(
        [
            call(f"Annotator: Person: {annotation.annotator.name} ({annotation.annotator.email})\n"),
            call("AnnotationDate: 2022-12-24T00:00:00Z\n"),
            call(f"AnnotationType: {annotation.annotation_type.name}\n"),
            call(f"SPDXREF: {annotation.spdx_id}\n"),
            call(f"AnnotationComment: {annotation.annotation_comment}\n"),
        ]
    )
