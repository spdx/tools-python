# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx3.model.licensing import ListedLicense, ListedLicenseException, WithAdditionOperator
from tests.spdx3.fixtures import fixture_factory


def test_valid_initialization():
    lic = fixture_factory(ListedLicense)
    lic_addition = fixture_factory(ListedLicenseException)
    with_addition_operator = WithAdditionOperator(lic, lic_addition)

    assert with_addition_operator.subject_license == lic


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        WithAdditionOperator("License", "LicenseAddition")

    assert len(err.value.args[0]) == 2
    for arg in err.value.args[0]:
        assert arg.startswith("SetterError WithAdditionOperator:")
