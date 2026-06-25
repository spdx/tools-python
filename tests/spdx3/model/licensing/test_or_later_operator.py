# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx3.model.expandedlicensing import ListedLicense, OrLaterOperator
from tests.spdx3.fixtures import creation_info_fixture, fixture_factory


def test_valid_initialization():
    lic = fixture_factory(ListedLicense)
    or_later_operator = OrLaterOperator(
        "https://spdx.test/tools-python/with_addition_operation", lic.spdx_id, creation_info_fixture()
    )

    assert or_later_operator.subject_license == lic.spdx_id


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        OrLaterOperator(123, "License", "creationInfo")  # type: ignore  # intentionally incorrect

    assert len(err.value.args[0]) == 2
    assert err.value.args[0][0].startswith("SetterError OrLaterOperator:")
