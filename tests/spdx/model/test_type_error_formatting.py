# SPDX-FileCopyrightText: 2026 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import sys

import pytest

from spdx_tools.common.typing.constructor_type_errors import ConstructorTypeErrors
from spdx_tools.spdx.model import Package, SpdxNoAssertion


@pytest.mark.parametrize("is_terminal", [True, False])
def test_constructor_errors_are_plain_text(monkeypatch, is_terminal):
    monkeypatch.setattr(sys.stdout, "isatty", lambda: is_terminal)

    with pytest.raises(ConstructorTypeErrors) as error:
        Package("SPDXRef-Package", "example", SpdxNoAssertion(), attribution_texts="invalid")

    messages = error.value.get_messages()
    assert len(messages) == 1
    assert "attribution_texts" in messages[0]
    assert "invalid" in messages[0]
    assert "\x1b" not in messages[0]


@pytest.mark.parametrize("is_terminal", [True, False])
def test_setter_errors_are_plain_text(monkeypatch, is_terminal):
    monkeypatch.setattr(sys.stdout, "isatty", lambda: is_terminal)
    package = Package("SPDXRef-Package", "example", SpdxNoAssertion())

    with pytest.raises(TypeError) as error:
        package.attribution_texts = "invalid"

    assert "attribution_texts" in str(error.value)
    assert "invalid" in str(error.value)
    assert "\x1b" not in str(error.value)
