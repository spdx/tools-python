# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

import pytest

from spdx_tools.spdx.model import ExtractedLicensingInfo


def test_correct_initialization():
    extracted_licensing_info = ExtractedLicensingInfo("id", "text", "name", ["reference"], "comment")
    assert extracted_licensing_info.license_id == "id"
    assert extracted_licensing_info.extracted_text == "text"
    assert extracted_licensing_info.license_name == "name"
    assert extracted_licensing_info.cross_references == ["reference"]
    assert extracted_licensing_info.comment == "comment"


def test_wrong_type_in_license_id():
    with pytest.raises(TypeError):
        ExtractedLicensingInfo(license_id=42)


def test_wrong_type_in_extracted_text():
    with pytest.raises(TypeError):
        ExtractedLicensingInfo(extracted_text=42)


def test_wrong_type_in_license_name():
    with pytest.raises(TypeError):
        ExtractedLicensingInfo(license_name=42)


def test_wrong_type_in_cross_references():
    with pytest.raises(TypeError):
        ExtractedLicensingInfo(cross_references=[41, 42])


def test_wrong_type_in_comment():
    with pytest.raises(TypeError):
        ExtractedLicensingInfo(comment=42)
