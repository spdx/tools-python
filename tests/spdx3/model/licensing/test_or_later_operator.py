# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx3.model.licensing import ListedLicense, OrLaterOperator
from tests.spdx3.fixtures import fixture_factory


def test_valid_initialization():
    lic = fixture_factory(ListedLicense)
    or_later_operator = OrLaterOperator(lic)

    assert or_later_operator.subject_license == lic


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        OrLaterOperator("License")

    assert len(err.value.args[0]) == 1
    assert err.value.args[0][0].startswith("SetterError OrLaterOperator:")
