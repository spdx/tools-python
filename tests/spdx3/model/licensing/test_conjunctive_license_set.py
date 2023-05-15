# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx3.model.licensing import ConjunctiveLicenseSet, ListedLicense
from tests.spdx3.fixtures import fixture_factory


def test_valid_initialization():
    lic = fixture_factory(ListedLicense)
    conjunctive_license_set = ConjunctiveLicenseSet([lic, lic])

    assert conjunctive_license_set.member == [lic, lic]


def test_invalid_initialization():
    lic = fixture_factory(ListedLicense)
    with pytest.raises(TypeError) as err:
        ConjunctiveLicenseSet(lic)

    assert len(err.value.args[0]) == 1
    assert err.value.args[0][0].startswith("SetterError ConjunctiveLicenseSet:")
