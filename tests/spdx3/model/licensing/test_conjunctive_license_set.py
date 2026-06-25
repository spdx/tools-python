# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx3.model.expandedlicensing import ConjunctiveLicenseSet, ListedLicense
from tests.spdx3.fixtures import creation_info_fixture, fixture_factory


def test_valid_initialization():
    lic = fixture_factory(ListedLicense)
    conjunctive_license_set = ConjunctiveLicenseSet(
        "https://spdx.test/tools-python/conjunctive-license-set", [lic.spdx_id, lic.spdx_id], creation_info_fixture()
    )

    assert conjunctive_license_set.member == [lic.spdx_id, lic.spdx_id]


def test_invalid_initialization():
    lic = fixture_factory(ListedLicense)
    with pytest.raises(TypeError) as err:
        ConjunctiveLicenseSet(123, lic, "creationInfo")  # type: ignore  # intentionally incorrect

    assert len(err.value.args[0]) == 3
    assert err.value.args[0][0].startswith("SetterError ConjunctiveLicenseSet:")
