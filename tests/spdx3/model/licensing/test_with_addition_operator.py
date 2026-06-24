# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx3.model.expandedlicensing import ListedLicense, ListedLicenseException, WithAdditionOperator
from tests.spdx3.fixtures import creation_info_fixture, fixture_factory


def test_valid_initialization():
    lic = fixture_factory(ListedLicense)
    lic_addition = fixture_factory(ListedLicenseException)
    with_addition_operator = WithAdditionOperator(
        "https://spdx.test/tools-python/with_addition_operation",
        lic.spdx_id,
        lic_addition.spdx_id,
        creation_info_fixture(),
    )

    assert with_addition_operator.subject_extendable_license == lic.spdx_id
    assert with_addition_operator.subject_addition == lic_addition.spdx_id


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        # intentionally incorrect
        WithAdditionOperator(123, "License", "LicenseAddition", "creationInfo")  # type: ignore

    assert len(err.value.args[0]) == 2
    for arg in err.value.args[0]:
        assert arg.startswith("SetterError WithAdditionOperator:")
