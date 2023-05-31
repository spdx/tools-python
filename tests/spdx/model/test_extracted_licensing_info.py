# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from spdx_tools.spdx.model import ExtractedLicensingInfo


def test_correct_initialization():
    extracted_licensing_info = ExtractedLicensingInfo("id", "text", "name", ["reference"], "comment")
    assert extracted_licensing_info.license_id == "id"
    assert extracted_licensing_info.extracted_text == "text"
    assert extracted_licensing_info.license_name == "name"
    assert extracted_licensing_info.cross_references == ["reference"]
    assert extracted_licensing_info.comment == "comment"
