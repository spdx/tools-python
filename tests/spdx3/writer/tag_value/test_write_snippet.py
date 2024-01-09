# SPDX-FileCopyrightText: 2024 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import io

from spdx_tools.spdx3.model.positive_integer_range import PositiveIntegerRange
from spdx_tools.spdx3.model.software import Snippet
from spdx_tools.spdx3.writer.console.software.snippet_writer import write_snippet


def test_render_creation_info():
    snippet = Snippet(
        spdx_id="SPDXRef-Snippet",
        byte_range=PositiveIntegerRange(0, 3),
        line_range=PositiveIntegerRange(1, 2),
    )
    output_str = io.StringIO()
    write_snippet(snippet, text_output=output_str)

    assert (
        output_str.getvalue()
        == """\
## Snippet
SPDXID: SPDXRef-Snippet
byte_range: 0:3
line_range: 1:2
"""
    )
